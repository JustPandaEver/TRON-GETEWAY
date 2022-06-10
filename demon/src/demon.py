from typing import Optional, Dict

import aiofiles
from tronpy.tron import TAddress
from tronpy.async_tron import AsyncTron, AsyncHTTPProvider

from src.types import CoinHelper
from config import LAST_BLOCK
from config import Config, logger


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

    async def get_node_block_number(self) -> int:
        """Get the number of the private block in the node"""
        try:
            return int(await self.node.get_latest_block_number())
        except Exception as error:
            logger.error(f"ERROR STEP 28: {error}")
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

    # @staticmethod
    async def smart_contract_transaction(self, data: str, contract_address: TAddress) -> Dict:
        """
        Unpacking a smart contract
        :param data: Smart Contract Information
        :param contract_address: Smart contract (Token TRC20) address
        """
        token_info = CoinHelper.get_token_by_address()

        self.node.to_base58check_address