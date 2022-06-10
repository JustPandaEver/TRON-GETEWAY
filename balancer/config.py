import os
import logging
import decimal

logger = logging.getLogger(__name__)

decimals = decimal.Context()
decimals.prec = 8


class Config:
    NETWORK = os.getenv("NETWORK", "TESTNET").upper()

    REDIS_URL = os.getenv("REDIS_URL")
    RABBITMQ_URL = os.getenv("RABBITMQ_URL")
    QUEUE_BALANCER = os.getenv("QUEUE_BALANCER", "balancer_messanger")

    NODE_URL = os.getenv("NODE_URL", "http://tron-mainnet.mangobank.elcorp.io:8090")
    HELPER_KEYS = "8d375175-fa31-490d-a224-63a056adb60b"

    ADMIN_ADDRESS = os.getenv("ADMIN_ADDRESS")
