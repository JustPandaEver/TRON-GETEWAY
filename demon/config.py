import os
import logging
import decimal

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(ROOT_DIR, "files")

LAST_BLOCK = os.path.join(BASE_DIR, "last_block.txt")
NOT_SEND = os.path.join(BASE_DIR, 'not_send')

if "files" not in os.listdir(ROOT_DIR):
    os.mkdir(BASE_DIR)
if 'not_send' not in os.listdir(BASE_DIR):
    os.mkdir(NOT_SEND)
if "last_block.txt" not in os.listdir(BASE_DIR):
    with open(LAST_BLOCK, "w") as file:
        file.write("")

decimals = decimal.Context()
decimals.prec = 8

logger = logging.getLogger(__name__)


class Config:
    NETWORK = os.getenv("NETWORK", "TESTNET").upper()

    RABBITMQ_URL = os.getenv("RABBITMQ_URL")
    QUEUE_BALANCER = os.getenv("QUEUE_BALANCER", "balancer_messanger")

    NODE_URL = os.getenv("NODE_URL", "http://tron-mainnet.mangobank.elcorp.io:8090")
    HELPER_KEYS = "8d375175-fa31-490d-a224-63a056adb60b"

    ADMIN_ADDRESS = os.getenv("ADMIN_ADDRESS")
