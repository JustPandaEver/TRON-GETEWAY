from asyncio import Lock
from typing import Tuple
from datetime import datetime, timedelta


lock = Lock()


class AddressesRepository:
    """Address repository - Serves for temporary storage of data for celery"""
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AddressesRepository, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__addresses = {}

    async def can_go(self, address) -> Tuple[bool, int]:
        async with lock:
            if address not in self.__addresses:
                self.__addresses.update({address: datetime.now()})
            seconds = (datetime.now() - self.__addresses[address]).seconds
            if seconds > 60:
                self.__addresses.update({address: datetime.now()})
                return True, 0
            else:
                self.__addresses.update({address: self.__addresses[address] + timedelta(seconds=60 - seconds)})
                return False, 60 - seconds


addresses_repository = AddressesRepository()
