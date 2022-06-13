import os
import logging
import decimal

logger = logging.getLogger(__name__)

decimals = decimal.Context()
decimals.prec = 8


class Config:
    NETWORK = os.getenv("NETWORK", "TESTNET").upper()
    API_URL = os.getenv("API_URL", "https://task-alexey-prsarev")

    REDIS_URL = os.getenv("REDIS_URL")
    RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqps://yubbvrbt:52cIr-IEy45n6hptj5n0aIT0LRn0cnZ6@goose.rmq2.cloudamqp.com/yubbvrbt")
    QUEUE_BALANCER = os.getenv("QUEUE_BALANCER", "balancer_messanger")

    NODE_URL = os.getenv("NODE_URL", "http://tron-mainnet.mangobank.elcorp.io:8090")
    HELPER_KEYS = "8d375175-fa31-490d-a224-63a056adb60b"

    ADMIN_ADDRESS = os.getenv("ADMIN_ADDRESS")
    TOKEN_COST_USDT = decimals.create_decimal(os.getenv("TOKEN_COST_USDT", "1.0"))
