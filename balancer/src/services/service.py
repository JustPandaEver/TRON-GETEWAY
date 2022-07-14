import json
from typing import Optional, Dict

import aiohttp
import aio_pika
from tronpy.tron import TAddress

from src.utils.types import BodySendToAlert
from src.utils.utils import utils, helper
from config import Config, logger


class Sender:
    """This class is used for sending data"""
    ADD_MONEY = Config.API_URL + "/add-user-money"

    @staticmethod
    def __get_headers() -> Dict:
        return {
            "Authorization": Config.BEARER_TOKEN
        }

    @staticmethod
    async def send_to_alert(body: BodySendToAlert) -> Optional:
        """Send a notification that the wallet has been replenished"""
        try:
            async with aiohttp.ClientSession(headers=Sender.__get_headers()) as session:
                async with session.post(
                    url=Sender.ADD_MONEY,
                    json=body.to_json
                ) as _:
                    logger.error(f"{utils.time_now()} | SEND TO ALERT THAN ADD MONEY: {body.address} | {_.ok}")
        except Exception as error:
            logger.error(f"{utils.time_now()} | ERROR STEP 44: {error}")

    @staticmethod
    async def resend_to_balancer(message: Dict) -> Optional:
        """In case of an error, resend the data"""
        connection: Optional[aio_pika.RobustConnection] = None
        try:
            connection = await aio_pika.connect_robust(url=Config.RABBITMQ_URL)
            channel = await connection.channel()
            await channel.declare_queue(Config.QUEUE_BALANCER, durable=True)
            await channel.default_exchange.publish(
                message=aio_pika.Message(body=json.dumps(message, default=utils.validate_json).encode()),
                routing_key=Config.QUEUE_BALANCER
            )
            logger.error(f"{utils.time_now()} | RESEND TO BALANCER: {message[0]} | Address: {message[1].get('address')}")
        except Exception as error:
            logger.error(f"{utils.time_now()} | ERROR STEP 51: {error}")
            await helper.write_to_error(error=str(error), step=22, message=str(message))
            await helper.write_to_not_send(message=message)
        finally:
            if connection is not None and not connection.is_closed:
                await connection.close()


class Getter:
    """This class is used to get data"""
    USER_PRIVATE_KEY = Config.API_URL + "/get-private-key/"

    @staticmethod
    def __get_headers() -> Dict:
        return {
            "Authorization": Config.BEARER_TOKEN
        }

    @staticmethod
    async def get_private_key(address: TAddress) -> str:
        """Get a private key at the wallet address"""
        try:
            async with aiohttp.ClientSession(headers=Getter.__get_headers()) as session:
                async with session.get(
                        url=Getter.USER_PRIVATE_KEY, param={'address': address}
                ) as response:
                    private_key = await response.json()
            if private_key.get("privateKey") is None:
                logger.error((
                    f'{utils.time_now()} '
                    f'| THE PRIVATE KEY FOR THIS ACCOUNT WAS NOT FOUND | ADDRESS: {address}'
                ))
                raise Exception
            return private_key.get("privateKey")
        except Exception as error:
            logger.error(f"{utils.time_now()} | ERROR STEP 18: {error}")
            raise error


sender = Sender
getter = Getter
