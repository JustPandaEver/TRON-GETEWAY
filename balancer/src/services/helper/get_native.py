import decimal

from src.utils.utils import utils
from src.utils.types import BodySendTransaction
from src.services.inc.node import node_tron
from config import Config, logger


async def get_native(address: str, amount: decimal.Decimal) -> bool:
    """Ask the central wallet for native currency to pay the commission!"""
    logger.error(f"{utils.time_now()} | ADMIN WALLET | SEND NATIVE TO PAY FEE | TO: {address} AMOUNT: {amount} TRX")
    status, tx_id = await node_tron.send_transaction(body=BodySendTransaction(
        fromAddress=Config.ADMIN_ADDRESS,
        fromPrivateKey=Config.ADMIN_PRIVATE_KEY,
        toAddress=address,
        amount=float(amount)
    ))
    if status:
        logger.error(f"{utils.time_now()} | ADMIN WALLET | THE NATIVE HAS BEEN SENT | TX ID: {tx_id}")
        return True
    else:
        logger.error(f"{utils.time_now()} | ADMIN WALLET | THE NATIVE WAS NOT SENT | TO: {address} AMOUNT: {amount} TRX")
        return False
