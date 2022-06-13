import os
import uuid
import json
import decimal
import base58
from typing import Any, Union, Optional, List, Tuple, Dict

import aiofiles
from tronpy.tron import TAddress

from src.helper.types import MAX_SUN, MIN_SUN, SUN
from config import NOT_SEND, ERROR, decimals as dml


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

    @staticmethod
    def correct_parser_data(_type: Any, data: str = None) -> Optional[Any]:
        if data is None:
            return None
        data = data.replace(" ", "")
        if _type == int and data.isdigit():
            return int(data)
        elif _type == list and len(data) > 30:
            if data.find(",") > 0:
                return list(filter(lambda x: x != "", data.split(",")))
            return [data]
        else:
            raise Exception("Something is wrong!")


class Helper:
    @staticmethod
    async def write_to_not_send(message: List[Dict]) -> Optional:
        async with aiofiles.open(os.path.join(NOT_SEND, f"{uuid.uuid4()}.json"), 'w') as file:
            await file.write(json.dumps(message))

    @staticmethod
    async def write_to_error(error: str, step: int, message: str = None) -> Optional:
        async with aiofiles.open(ERROR, 'a', encoding='utf-8') as file:
            await file.write(f"{error} STEP {step} | MESSAGE: {message if message is not None else '~Not message~'}")
