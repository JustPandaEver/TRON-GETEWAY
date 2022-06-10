from tronpy.tron import TAddress

from src.services.node import node_tron
from src.helper.types import BodyOptimalFee
from src.helper.types import CoinHelper
from config import Config, logger


class SENDERHelper:
    pass


async def send_to_wallet_to_wallet(address: TAddress, token: str):
    try:
        balance_token = await node_tron.balance(address=address, token=token)
        logger.error(
            f"==> {token.upper()} | ADDRESS: {address} | BALANCE: {balance_token} | PREPARING TO EMPTY THE BALANCE"
        )
        if balance_token < CoinHelper.get_token(symbol=token):
            logger.error(
                f"==> {token.upper()} | ADDRESS: {address} | "
                f"BALANCE: {balance_token} | NOT SUITABLE FOR BALANCE TRANSFER!!"
            )
            return None
        fee = await node_tron.optimal_fee(
            body=BodyOptimalFee(fromAddress=address, toAddress=Config.ADMIN_ADDRESS, symbol=token)
        )
        balance_native = await node_tron.balance(address=address)
        if balance_native - fee <= 0:
            logger.error(f"==> {token.upper()} | ADDRESS {address} | THERE IS NOT ENOUGH TRX BALANCE TO TRANSFER!!!")

    except Exception as error:
        logger.error(f"ERROR: {error}")
    finally:
        pass

