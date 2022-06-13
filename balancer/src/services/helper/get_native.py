from src.utils.utils import utils
from src.utils.types import BodySendTransaction
from src.services.inc.node import node_tron
from config import Config, logger


async def get_native(address: str, amount: float) -> bool:
    logger.error(f"{utils} | ADMIN WALLET | SEND NATIVE TO PAY FEE | TO: {address} AMOUNT: {amount} TRX")
    status, tx_id = node_tron.send_transaction(body=BodySendTransaction(
        fromAddress=Config.ADMIN_ADDRESS,
        fromPrivateKey=Config.ADMIN_PRIVATE_KEY,
        toAddress=address,
        amount=amount
    ))
    if status:
        logger.error(f"{utils} | ADMIN WALLET | THE NATIVE HAS BEEN SENT | TX ID: {tx_id}")
        return True
    else:
        logger.error(f"{utils} | ADMIN WALLET | THE NATIVE WAS NOT SENT | TO: {address} AMOUNT: {amount} TRX")
        return False
