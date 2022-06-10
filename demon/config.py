import os
import logging
import decimal


decimals = decimal.Context()
decimals.prec = 8

logger = logging.getLogger(__name__)


class Config:
    NETWORK = os.getenv("NETWORK", "TESTNET").upper()

    RABBITMQ_URL = os.getenv("RABBITMQ_URL")
    QUEUE_BALANCER = os.getenv("QUEUE_BALANCER")

    NODE_URL = os.getenv("NODE_URL")

    ADMIN_ADDRESS = os.getenv("ADMIN_ADDRESS")
