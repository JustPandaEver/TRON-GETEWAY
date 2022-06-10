import decimal
from dataclasses import dataclass
from typing import Optional, Tuple

from tronpy.tron import TAddress

from config import Config


SUN = decimal.Decimal("1000000")
MIN_SUN = 0
MAX_SUN = 2**256 - 1

USDT_ADDRESS = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t" \
    if Config.NETWORK == "mainnet" \
    else "TRvz1r3URQq5otL7ioTbxVUfim9RVSm1hA"

USDT_INFO = {"bd": 345, "f": 100, "nb": 14631, "hb": 29631} \
    if Config.NETWORK == "mainnet" \
    else {"bd": 345, "f": 10, "nb": 14631, "hb": 29631}


class CoinHelper:
    # (symbol, address, decimals)
    USDT = ("USDT", USDT_ADDRESS, 10**6, USDT_INFO)

    @staticmethod
    def get_token(symbol: str) -> Optional[Tuple[str, TAddress, int]]:
        return CoinHelper.__dict__.get(symbol)


# <<<======================================>>> DATACLASSES <<<=======================================================>>>


@dataclass
class BodyOptimalFee:
    fromAddress: TAddress
    toAddress: TAddress
    symbol: Optional[str] = None


@dataclass
class BodySendTransaction:
    fromAddress: TAddress
    fromPrivateKey: str
    toAddress: TAddress
    amount: float
    symbol: Optional[str] = None
