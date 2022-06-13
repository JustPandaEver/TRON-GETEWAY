from decimal import Decimal
from typing import Optional, List, Tuple, Dict

from tronpy.tron import TAddress

from src.services.inc.node import node_tron
from src.services.helper.get_native import get_native
from src.services.service import getter, sender
from src.utils.exception import NotFeeResend
from src.utils.utils import utils
from src.utils.types import User, BodyOptimalFee
from src.utils.types import CoinHelper
from config import Config, logger


class UserValidator:
    def __init__(self, user: User):
        self.address = user.address
        self.private_key = user.privateKey

    async def validate_token_balance(self, token: str) -> Tuple[bool, Decimal]:
        balance = await node_tron.balance(address=self.address, symbol=token)
        if token is not None and balance < CoinHelper.min_cost(symbol=token):
            return False, balance
        return True, balance

    async def validate_fee(self, token: str = None) -> Tuple[bool, Decimal, Decimal]:
        balance_native = await node_tron.balance(address=self.address)
        fee = node_tron.optimal_fee(body=BodyOptimalFee(
            fromAddress=self.address, toAddress=Config.ADMIN_ADDRESS, symbol=token
        ))
        if balance_native - fee <= 0:
            return False, fee, balance_native
        return True, fee, balance_native




async def send_to_wallet_to_wallet(address: TAddress, token: str, message: List[Dict]) -> Optional:
    try:
        user = UserValidator(user=User(
            address=address,
            privateKey=await getter.get_private_key(address)
        ))
        valid_balance, balance = await user.validate_token_balance(token=token)
        if not valid_balance:
            logger.error((
                f"{utils.time_now()} | "
                f"ADDRESS: {address} | THE USER'S BALANCE IS TOO SMALL TO START FORWARDING! | "
                f"USER BALANCE: {balance} {token}"
            ))
            return
        valid_fee, fee, balance_native = await user.validate_fee(token=token)
        if not valid_fee:
            logger.error((
                f"{utils.time_now()} | "
                f"ADDRESS: {address} | THE USER DOES NOT HAVE ENOUGH FUNDS TO PAY THE COMMISSION | "
                f"USER BALANCE: {balance_native} TRX | FEE PRICE {fee} TRX"
            ))
            if not await get_native(address, amount=fee):
                raise NotFeeResend(f'{utils.time_now()} | THE NATIVE HAS BEEN SENT | TO: {address}')


    except Exception as error:
        logger.error(f"ERROR STEP 41: {error}")

    finally:
        pass

