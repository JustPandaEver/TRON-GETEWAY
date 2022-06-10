import asyncio
import decimal
from time import time as timer
from datetime import datetime, timedelta
from typing import Optional, Tuple, List, Dict

import aiofiles
from tronpy.tron import TAddress
from tronpy.async_tron import AsyncTron, AsyncHTTPProvider

from src.services.service import Sender, Getter, send_all_from_folder_not_send
from src.helper.utils import Utils
from src.helper.types import HeadMessage, BodyMessage
from src.helper.types import BodyRun, BodyProcessingTransaction, BodySendBalancer, BodyTransaction
from src.helper.types import CoinHelper
from config import LAST_BLOCK
from config import Config, decimals, logger


class TransactionDemon:
    """Tron demon"""
    def __init__(self):
        self.node: Optional[AsyncTron] = None
        self.public_node: Optional[AsyncTron] = None
        self.connect()

    def connect(self):
        network = "mainnet" if Config.NODE_URL != "TESTNET" else "shasta"
        self.node: AsyncTron = AsyncTron(
            provider=AsyncHTTPProvider(Config.NODE_URL) if network == "mainnet" else None,
            network=network
        )
        self.public_node: AsyncTron = AsyncTron(
            provider=AsyncHTTPProvider(api_key=Config.HELPER_KEYS) if network == "mainnet" else None,
            network=network
        )

    # <<<===================================>>> Block/Transaction Helper <<<=========================================>>>

    async def get_node_block_number(self) -> int:
        """Get the number of the private block in the node"""
        try:
            return int(await self.node.get_latest_block_number())
        except Exception as error:
            logger.error(f"ERROR STEP 36: {error}")
            return int(await self.public_node.get_latest_block_number())

    async def get_last_block_number(self) -> int:
        """Get the block number recorded in the "last_block.txt" file"""
        async with aiofiles.open(LAST_BLOCK, "r") as file:
            last_block = await file.read()
        if last_block:
            return int(last_block)
        return await self.get_node_block_number()

    @staticmethod
    async def save_block_number(block_number: int) -> Optional:
        """
        Save the current block to a file "last_block.txt"
        :param block_number: The number of the block to be recorded
        """
        async with aiofiles.open(LAST_BLOCK, "w") as file:
            await file.write(str(block_number))

    async def get_block_and_count(self, block_number: int) -> Tuple[Optional[Dict], int]:
        try:
            block = await self.node.get_block(id_or_num=block_number)
        except Exception as error:
            logger.error(f"ERROR: {error}")
            block = await self.public_node.get_block(id_or_num=block_number)
        if "transactions" in block.keys() and isinstance(block["transactions"], list):
            return block, len(block["transactions"])
        return None, 0

    async def get_transaction_fee(self, transaction_hash: str) -> decimal.Decimal:
        try:
            transaction = await self.node.get_transaction_info(transaction_hash)
        except Exception as error:
            logger.error(f"ERROR STEP 74: {error}")
            transaction = await self.public_node.get_transaction_info(transaction_hash)
        if "fee" not in transaction:
            return decimals.create_decimal(0)
        return decimals.create_decimal(Utils.from_sun(transaction["fee"]))

    # <<<===================================>>> Smart Contract Helper <<<============================================>>>

    @staticmethod
    def smart_contract_transaction(data: str, contract_address: TAddress) -> Tuple[str, TAddress, decimal.Decimal]:
        """
        Unpacking a smart contract
        :param data: Smart Contract Information
        :param contract_address: Smart contract (Token TRC20) address
        """
        token_info = CoinHelper.get_token_by_address(address=contract_address)
        address, amount = Utils.convert_data(data=data, decimals=token_info[2])
        return token_info[0], address, amount

    # <<<===================================>>> Main Methods <<<=====================================================>>>

    async def processing_block(self, block_number: int, addresses: List[TAddress]) -> bool:
        """
        This method receives transactions from the block and processes them
        :param block_number: The number of the block from which to receive transactions
        :param addresses: A list of addresses to search for transactions
        """
        try:
            logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | PROCESSING BLOCK: {block_number}")
            block, count_txn = await self.get_block_and_count(block_number=block_number)
            if count_txn > 0:
                transactions = await asyncio.gather(*[
                    self.processing_transaction(body=BodyProcessingTransaction(
                        transaction=block["transactions"][index],
                        addresses=addresses,
                        timestamp=block["block_header"]["raw_data"]["timestamp"],
                    ))
                    for index in range(count_txn)
                ])
                transactions = list(filter(lambda x: x is not None, transactions))
                if len(transactions) > 0:
                    await asyncio.gather(*[
                        TransactionDemon.send_to_balancer(body=BodySendBalancer(
                            package=transaction,
                            addresses=addresses,
                            block_number=block_number
                        ))
                        for transaction in transactions
                    ])
            else:
                logger.error(f"BLOCK: {block_number} IS CLEAR!")
            return True
        except Exception as error:
            logger.error(f"ERROR STEP 76: {error}")
            return False

    async def processing_transaction(self, body: BodyProcessingTransaction) -> Optional[BodyMessage]:
        """
        This method analyzes transactions in detail, and searches for the necessary addresses in them.
        """
        try:
            # If the transaction is not confirmed or with an error, then skip it.
            if body.transaction["ret"][0]["contractRet"] != "SUCCESS":
                return None
            # Value in the transaction
            transaction_value = body.transaction["raw_data"]["contract"][0]["parameter"]["value"]
            # Transaction type
            transaction_type = body.transaction["raw_data"]["contract"][0]["type"]
            # Addresses that are in the transaction | Sender/s | Receiver/s
            transaction_addresses, from_address, to_address = [], None, None
            if transaction_value["owner_address"] is not None:
                # Recording the sender
                from_address = Utils.to_base58check_address(transaction_value["owner_address"])
                transaction_addresses.append(from_address)
            if transaction_type == "TransferContract" and transaction_value["to_address"] is not None:
                # We record the recipient if the transaction was made in the native currency.
                to_address = Utils.to_base58check_address(transaction_value["to_address"])
                transaction_addresses.append(to_address)
            elif transaction_type == "TriggerSmartContract" and CoinHelper.is_token(transaction_value["contract_address"]) \
                    and transaction_value["data"] is not None and 140 > len(transaction_value["data"]) > 130:
                # We record the recipient if the transaction was made in tokens.
                to_address = Utils.to_base58check_address("41" + transaction_value["data"][32:72])
                transaction_addresses.append(to_address)

            address = None
            for transaction_address in transaction_addresses:
                # We are looking for the address of our wallet among the addresses in the transaction.
                if transaction_address in body.addresses and Config.ADMIN_ADDRESS not in transaction_address:
                    # If we find it, we write it to a variable.
                    address = transaction_address
                    break

            if address is not None:
                if transaction_type == "TransferContract":
                    amount, symbol = decimals.create_decimal(Utils.from_sun(transaction_value["amount"])), "TRX"
                elif transaction_type == "TriggerSmartContract":
                    symbol, _, amount = TransactionDemon.smart_contract_transaction(
                        data=transaction_value["data"],
                        contract_address=transaction_value["contract_address"]
                    )
                else:
                    amount, symbol = 0, "TRX"
                return BodyMessage(address=address, transactions=[BodyTransaction(
                    timestamp=body.timestamp,
                    transactionHash=body.transaction["txID"],
                    amount=amount,
                    fee=float(await self.get_transaction_fee(body.transaction["txID"])),
                    inputs=[{from_address: amount}],
                    outputs=[{to_address: amount}],
                    token=symbol
                )])
            return None
        except Exception as error:
            logger.error(f"ERROR STEP 30: {error}")
            return None

    # <<<===================================>>> Sender Methods <<<===================================================>>>

    @staticmethod
    async def send_to_balancer(body: BodySendBalancer) -> Optional:
        """
        We are preparing transactions to be sent to RabbitMQ
        """
        return Sender.send_to_balancer(message=[
            # Head
            HeadMessage(
                network=f"TRON-{body.package.transactions[0].token.upper()}", block_number=body.block_number
            ).to_json,
            # Body
            body.package.to_json
        ])

    # <<<===================================>>> Run Methods <<<======================================================>>>

    async def run(self):
        """The script runs all the time"""
        start = await self.get_last_block_number()
        pack_size = 1
        while True:
            end = await self.get_node_block_number()
            if end - start < pack_size:
                await asyncio.sleep(3)
            else:
                start_time = timer()
                addresses = await Getter.get_addresses()
                success = await asyncio.gather(*[
                    self.processing_block(block_number=block_number, addresses=addresses)
                    for block_number in range(start, start + pack_size)
                ])
                logger.error("END BLOCK: {} | TIME TAKEN: {} SEC".format(
                    start, str(timedelta(seconds=timer() - start_time)))
                )
                if all(success):
                    start += pack_size
                    await self.save_block_number(block_number=start)

    # <<<===================================>>> Start Methods <<<====================================================>>>

    async def start_in_range(self, start: int, end: int, addresses: List[TAddress] = None) -> Optional:
        for block_number in range(start, end+1):
            if addresses is None:
                addresses = await Getter.get_addresses()
            await self.processing_block(block_number=int(block_number), addresses=addresses)

    async def start_in_list(self, list_blocks: List[int], addresses: List[TAddress] = None) -> Optional:
        for block_number in list_blocks:
            if addresses is None:
                addresses = await Getter.get_addresses()
            await self.processing_block(block_number=int(block_number), addresses=addresses)

    async def start(self, body: BodyRun) -> Optional:
        logger.error("START OF THE SEARCH\nSTART: {}\nEND: {}".format(body.start, body.end))
        if body.list_blocks:
            await self.start_in_list(list_blocks=body.list_blocks, addresses=body.addresses)
        elif body.start and body.end:
            await self.start_in_range(body.start, body.end, addresses=body.addresses)
        elif body.start and not body.end:
            await self.start_in_range(body.start, end=await self.get_node_block_number(), addresses=body.addresses)
        elif not body.start and body.end:
            await self.start_in_range(await self.get_node_block_number(), end=body.end, addresses=body.addresses)
        else:
            await send_all_from_folder_not_send()
            await self.run()
        logger.error("END OF SEARCH")
