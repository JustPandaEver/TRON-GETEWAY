from typing import Optional, List, Dict

from tronpy.tron import TAddress

from src.utils.types import BodySendToAlert
from src.utils.utils import helper
from config import logger


class Getter:
    @staticmethod
    async def get_private_key(address: TAddress) -> str:
        pass


class Sender:
    @staticmethod
    async def send_to_alert(body: BodySendToAlert):
        pass

    @staticmethod
    async def resend_to_balancer(message: List[Dict]) -> Optional:
        try:
            pass
        except Exception as error:
            logger.error(f"ERROR STEP 22: {error}")
            await helper.write_to_error(error=str(error), step=22, message=str(message))
            await helper.write_to_not_send(message=message)


getter = Getter
sender = Sender
