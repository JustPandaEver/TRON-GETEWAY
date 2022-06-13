from typing import List, Dict

from tronpy.tron import TAddress

from src.services.resend import send_to_wallet_to_wallet


async def send_transaction_service(address: TAddress, token: str, message: List[Dict]):
    await send_to_wallet_to_wallet(address=address, token=token, message=message)
