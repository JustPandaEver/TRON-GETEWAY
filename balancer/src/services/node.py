import decimal
from typing import Optional

from tronpy.tron import TAddress
from tronpy.exceptions import AddressNotFound
from tronpy.async_tron import AsyncTron, AsyncHTTPProvider

from src.helper.types import CoinHelper
from config import Config, decimals


class NodeTRON:
    """TRON NODE"""
    __PROVIDER = AsyncHTTPProvider(Config.NODE_URL)
    NETWORK = "mainnet" if Config.NETWORK == "MAINNET" else "shasta"

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(NodeTRON, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.node: AsyncTron = AsyncTron(
            provider=self.__PROVIDER if self.NETWORK == "mainnet" else None,
            network=self.NETWORK
        )
        self.public_node: AsyncTron = AsyncTron(
            provider=AsyncHTTPProvider(api_key=Config.HELPER_KEYS) if self.NETWORK == "mainnet" else None,
            network=self.NETWORK
        )

    def get_balance(self, address: TAddress, symbol: Optional[str] = None) -> decimal.Decimal:
        """Wallet balance"""
        if symbol is None:
            try:
                balance = await self.node.get_account_balance(addr=address)
            except AddressNotFound:
                balance = 0
        else:
            _, address, dml = CoinHelper.get_token(symbol=symbol)
            contract = await self.node.get_contract(address)
            if int(await contract.functions.balanceOf(address)) > 0:
                balance = int(await contract.functions.balanceOf(address)) / dml
            else:
                balance = 0
        return decimals.create_decimal(balance)
