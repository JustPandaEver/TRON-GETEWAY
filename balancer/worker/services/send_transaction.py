from tronpy.tron import TAddress

from src.services.sender import send_to_wallet_to_wallet


async def send_transaction_service(address: TAddress, token: str):
    await send_to_wallet_to_wallet(address=address, token=token)
