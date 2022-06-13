import os
import uuid
import json
import decimal
from datetime import datetime
from typing import Any, Optional, Union, List, Dict

import aiofiles

from src.utils.types import MIN_SUN, MAX_SUN, SUN
from config import NOT_RESEND, ERROR


class Utils:
    @staticmethod
    def to_sun(num: Union[int, float]) -> int:
        """
        Helper function that will convert a value in TRX to SUN
        :param num: Value in TRX to convert to SUN
        """
        if isinstance(num, int) or isinstance(num, str):
            d_num = decimal.Decimal(value=num)
        elif isinstance(num, float):
            d_num = decimal.Decimal(value=str(num))
        elif isinstance(num, decimal.Decimal):
            d_num = num
        else:
            raise TypeError("Unsupported type. Must be one of integer, float, or string")
        s_num = str(num)
        unit_value = SUN
        if d_num == 0:
            return 0
        if d_num < 1 and "." in s_num:
            with decimal.localcontext() as ctx:
                multiplier = len(s_num) - s_num.index(".") - 1
                ctx.prec = multiplier
                d_num = decimal.Decimal(value=num, context=ctx) * 10 ** multiplier
            unit_value /= 10 ** multiplier
        with decimal.localcontext() as ctx:
            ctx.prec = 999
            result = decimal.Decimal(value=d_num, context=ctx) * unit_value
        if result < MIN_SUN or result > MAX_SUN:
            raise ValueError("Resulting wei value must be between 1 and 2**256 - 1")
        return int(result)

    @staticmethod
    def time_now(timestep: bool = False) -> Union[int, datetime]:
        """Get the current time"""
        date = datetime.now()
        if timestep:
            return int(datetime.timestamp(date))
        return date

    @staticmethod
    def validate_json(obj: Any):
        """For json default"""
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return obj


class Helper:
    @staticmethod
    async def write_to_not_send(message: Union[Dict, List[Dict]]) -> Optional:
        """Record data about an unsent transaction"""
        async with aiofiles.open(os.path.join(NOT_RESEND, f"{uuid.uuid4()}.json"), 'w') as file:
            await file.write(json.dumps(message, default=utils.validate_json))

    @staticmethod
    async def write_to_error(error: str, step: int, message: str = None) -> Optional:
        """Record error information"""
        async with aiofiles.open(ERROR, 'a', encoding='utf-8') as file:
            await file.write(
                f"ERROR: {error} | STEP {step} | MESSAGE: {message if message is not None else '~Not message~'}\n"
            )


utils = Utils
helper = Helper
