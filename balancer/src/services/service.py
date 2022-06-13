from typing import List, Dict

from tronpy.tron import TAddress


class Getter:
    @staticmethod
    async def get_private_key(address: TAddress) -> str:
        pass


class Sender:
    @staticmethod
    async def send_to_alert(body):
        pass

    @staticmethod
    async def resend_to_balancer(message: List[Dict]):
        pass


getter = Getter
sender = Sender
