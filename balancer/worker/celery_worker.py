import asyncio
from typing import List, Dict

from tronpy.tron import TAddress

from worker.celery_app import celery_app
from .services.send_transaction import send_transaction_service


def run_sync(f):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(f)


@celery_app.task(acks_late=True)
def send_transaction(address: TAddress, token: str, message: List[Dict]):
    run_sync(send_transaction_service(address=address, token=token, message=message))
