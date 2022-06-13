import decimal
from dataclasses import dataclass
from typing import Optional, Tuple, Dict

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
    # (symbol, address, decimals, token_ifno)
    USDT = ("USDT", USDT_ADDRESS, 10**6, USDT_INFO)
    COST = {"USDT": Config.TOKEN_COST_USDT}

    @staticmethod
    def get_token(symbol: str) -> Optional[Tuple[str, TAddress, int]]:
        """Get information about the token"""
        return CoinHelper.__dict__.get(symbol)

    @staticmethod
    def min_cost(symbol: str) -> decimal.Decimal:
        """Get the price for the minimum transfer to the main wallet"""
        return CoinHelper.COST.get(symbol)


# <<<======================================>>> DATACLASSES <<<=======================================================>>>


class ToJson:
    """Object to json"""
    @property
    def to_json(self) -> Dict:
        raise NotImplementedError


@dataclass
class User:
    """User model"""
    address: TAddress                   # Wallet address
    privateKey: str                     # Wallet private key


@dataclass
class BodyOptimalFee:
    """For optimal fee func"""
    fromAddress: TAddress               # Sender's wallet address
    toAddress: TAddress                 # Receiver's wallet address
    symbol: Optional[str] = None        # Token name. Example: USDT


@dataclass
class BodySendTransaction:
    """For send transaction func"""
    fromAddress: TAddress               # Sender's wallet address
    fromPrivateKey: str                 # Sender's wallet private key
    toAddress: TAddress                 # Receiver's wallet address
    amount: float                       # Transaction amount
    symbol: Optional[str] = None        # Token name. Example: USDT


@dataclass
class BodySendToAlert(ToJson):
    """For send to alert"""
    timestamp: int                      # The time of creation of the transfer to the main wallet
    transactionHash: str                # Transaction hash
    address: TAddress                   # The address of the wallet whose balance needs to be replenished
    amount: float                       # The amount you need to top up

    @property
    def to_json(self) -> Dict:
        raise self.__dict__
