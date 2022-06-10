import decimal
from typing import Optional, Tuple

from tronpy.tron import TAddress

from config import Config


SUN = decimal.Decimal("1000000")
MIN_SUN = 0
MAX_SUN = 2**256 - 1

USDT_ADDRESS = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t" \
    if Config.NETWORK == "mainnet" \
    else "TRvz1r3URQq5otL7ioTbxVUfim9RVSm1hA"


class CoinHelper:
    # (symbol, address, decimals)
    USDT = ("USDT", USDT_ADDRESS, 10**6)
    TOKENS = {USDT_ADDRESS: USDT}

    @staticmethod
    def get_token_by_address(address: TAddress) -> Optional[Tuple[str, TAddress, int]]:
        return CoinHelper.TOKENS.get(address)
