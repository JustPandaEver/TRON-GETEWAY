import json
import os
from typing import Optional, List, Dict

import aiofiles
import aio_pika
import requests
from tronpy.tron import TAddress

from config import NOT_SEND
from config import Config, logger


async def send_all_from_folder_not_send():
    """Send those transits that were not sent due to any errors"""
    files = os.listdir(NOT_SEND)
    for file_name in files:
        try:
            path = os.path.join(NOT_SEND, file_name)
            async with aiofiles.open(path, 'r') as file:
                message = list(await file.read())
            await Sender.send_to_balancer(message=message)
            os.remove(path)
        except Exception as error:
            logger.error("ERROR: {}\nNOT SEND: {}".format(error, file_name))
            continue


class Sender:
    @staticmethod
    async def send_to_balancer(message: List[Dict]):
        """Send transaction to Balancer"""
        connection: Optional[aio_pika.RobustConnection] = None
        channel: Optional[aio_pika.RobustChannel] = None
        try:
            connection = await aio_pika.connect_robust(url=Config.RABBITMQ_URL)
            channel = await connection.channel()
            await channel.declare_queue(Config.QUEUE_BALANCER)
            await channel.default_exchange.publish(
                message=aio_pika.Message(body=json.dumps(message).encode()),
                routing_key=Config.QUEUE_BALANCER
            )
        except Exception as error:
            logger.error(f"ERROR: {error}")
        finally:
            if connection is not None and not connection.is_closed:
                await connection.close()


class Getter:
    @staticmethod
    async def get_addresses() -> List[TAddress]:
        pass

    @staticmethod
    def get_all_blocks_by_list_addresses(addresses: List[TAddress]) -> List[int]:
        blocks = []
        for address in addresses:
            response = requests.get(
                url=f"https://api.{'' if Config.NETWORK == 'mainnet' else 'shasta.'}trongrid.io/v1/accounts/{address}/transactions?limit=200",
                headers={"Accept": "application/json", "TRON-PRO-API-KEY": "16c3b7ca-d498-4314-aa1d-a224135faa26"}
            ).json()
            if "data" in response and len(response["data"]) > 0:
                blocks.extend(sorted([block["blockNumber"] for block in response["data"]]))
        return sorted(list(set(blocks)))
