import decimal
import base58
from typing import Union, List, Tuple, Dict

from tronpy.tron import TAddress

from src.types import MAX_SUN, MIN_SUN, SUN
from config import decimals as dml


class Utils:
    @staticmethod
    def to_base58check_address(raw_address: Union[str, bytes]) -> TAddress:
        if isinstance(raw_address, (str,)):
            if raw_address[0] == "T" and len(raw_address) == 34:
                try:
                    # assert checked
                    base58.b58decode_check(raw_address)
                except ValueError:
                    raise Exception("bad base58check format")
                return raw_address
            elif len(raw_address) == 42:
                if raw_address.startswith("0x"):  # eth address format
                    return base58.b58encode_check(b"\x41" + bytes.fromhex(raw_address[2:])).decode()
                else:
                    return base58.b58encode_check(bytes.fromhex(raw_address)).decode()
            elif raw_address.startswith("0x") and len(raw_address) == 44:
                return base58.b58encode_check(bytes.fromhex(raw_address[2:])).decode()
        elif isinstance(raw_address, (bytes, bytearray)):
            if len(raw_address) == 21 and int(raw_address[0]) == 0x41:
                return base58.b58encode_check(raw_address).decode()
            if len(raw_address) == 20:  # eth address format
                return base58.b58encode_check(b"\x41" + raw_address).decode()
            return Utils.to_base58check_address(raw_address.decode())
        raise Exception(repr(raw_address))

    @staticmethod
    def from_sun(num: Union[int, float]) -> Union[int, decimal.Decimal]:
        """
        Helper function that will convert a value in TRX to SUN
        :param num: Value in TRX to convert to SUN
        """
        if num == 0:
            return 0
        if num < MIN_SUN or num > MAX_SUN:
            raise ValueError("Value must be between 1 and 2**256 - 1")
        with decimal.localcontext() as ctx:
            ctx.prec = 999
            d_num = decimal.Decimal(value=num, context=ctx)
            result = d_num / SUN
        return result

    @staticmethod
    def convert_data(data: str, decimals: int) -> Tuple[TAddress, decimal.Decimal]:
        return (
            Utils.to_base58check_address("41"+data[32:72]),
            dml.create_decimal(int("0x"+data[72], 0) / decimals)
        )
