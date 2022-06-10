import decimal
from typing import Union

from src.helper.types import MIN_SUN, MAX_SUN, SUN


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
