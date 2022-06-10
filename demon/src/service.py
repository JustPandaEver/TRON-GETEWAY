import os
from typing import List, Dict

import aiofiles

from config import NOT_SEND, logger


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
        pass


class Getter:
    @staticmethod
    async def get_addresses():
        pass
