import decimal
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict

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

    @staticmethod
    def is_token(address: TAddress) -> bool:
        return address in [USDT_ADDRESS]


# <<<==========================================>>> RUN <<<===========================================================>>>

@dataclass
class BodyRun:
    start: Optional[int] = None
    end: Optional[int] = None
    list_blocks: Optional[List[int]] = None
    addresses: Optional[List[TAddress]] = None


# <<<==========================================>>> DATACLASSES <<<===================================================>>>


class ToJson:
    @property
    def to_json(self) -> Dict:
        raise NotImplementedError


@dataclass
class BodyProcessingTransaction:
    """For func processing transaction"""
    transaction: Dict                       # The transaction that needs to be parsed
    addresses: List[TAddress]               # A list of addresses to search for transactions
    timestamp: int                          # The time of confirmation of the transaction in the block


@dataclass
class BodyTransaction(ToJson):
    """Transaction"""
    timestamp: int                          # The time of confirmation of the transaction in the block
    transactionHash: str                    # Transaction hash
    amount: float                           # Transaction amount
    fee: float                              # Transaction fee
    inputs: List[Dict[str, float]]          # Sender/s
    outputs: List[Dict[str, float]]         # Recipient/s
    token: Optional[str] = None             # Token name

    @property
    def to_json(self) -> Dict:
        if self.token == "TRX":
            del self.token
        return self.__dict__


@dataclass
class HeadMessage(ToJson):
    """Head message for balancer"""
    network: str                            # Network. Example: TRON-USDT, TRON-TRX
    block_number: int                       # Block number

    @property
    def to_json(self) -> Dict:
        return self.__dict__


@dataclass
class BodyMessage(ToJson):
    """Body message for balancer"""
    address: TAddress                       # Our wallet that participated in the transaction
    transactions: List[BodyTransaction]     # Transactions found in the block

    @property
    def to_json(self) -> Dict:
        return {
            "address": self.__dict__.get("address"),
            "transactions": [transaction.to_json for transaction in self.__dict__.get("transactions")]
        }


@dataclass
class BodySendBalancer:
    """For func send to balancer"""
    package: BodyMessage                    # Packaged Message
    addresses: List[TAddress]               # Addresses of our wallets
    block_number: int                       # Block number
