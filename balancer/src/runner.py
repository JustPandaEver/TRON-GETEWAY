import json
import asyncio
from typing import Optional, List, Dict

import aio_pika

from src.utils.repository import addresses_repository
from worker.celery_app import celery_app
from config import Config, logger


async def processing_message(message: aio_pika.IncomingMessage):
    """
    Decrypt the message from the queue and send it for forwarding.
    :param message: Message from queue
    """
    async with message.process():
        msg: List[Dict, Dict] = json.loads(message.body)
        logger.error(f"GET INIT MESSAGE: {message}")
        head, body = msg
        token = head.get("network").split("-")[0]
        address = body.get("address")
        can_go, wait_time = await addresses_repository.can_go(address)
        extra = {"countdown": wait_time} if not can_go and wait_time > 5 else {}
        celery_app.send_task(f'worker.celery_worker.send_transaction', args=[address, token], **extra)


async def run(loop):
    while True:
        try:
            connection: Optional[aio_pika.RobustConnection]  = None
            while connection is None or connection.is_closed:
                try:
                    # Connect to RabbitMQ by url
                    connection: aio_pika.RobustConnection = await aio_pika.connect_robust(
                        Config.RABBITMQ_URL, loop=loop
                    )
                finally:
                    logger.error(f'WAIT CONNECT TO RABBITMQ')
                await asyncio.sleep(2)
            async with connection:
                # Connect to the RabbitMQ channel
                channel: aio_pika.Channel = await connection.channel()
                # Connections to the queue in RabbitMQ by name.
                __queue = await channel.declare_queue(Config.QUEUE_BALANCER, durable=True)
                async with __queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        await processing_message(message=message)
        except Exception as error:
            logger.error(f"ERROR STEP : {error}")
