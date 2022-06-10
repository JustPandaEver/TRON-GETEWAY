import sys
import argparse
import asyncio
from typing import Optional

from src.demon import TransactionDemon
from src.services.service import Getter
from src.helper.utils import Utils
from src.helper.types import BodyRun
from config import logger


class Parser:
    @staticmethod
    def create_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--start", default=None)
        parser.add_argument("-e", "--end", default=None)
        parser.add_argument("-b", "--blocks", default=None)
        parser.add_argument("-a", "--addresses", default=None)
        return parser

    @staticmethod
    async def run(data: BodyRun) -> Optional:
        """Run search script"""
        demon: Optional[TransactionDemon] = None
        try:
            demon = TransactionDemon()
            if data.start or data.end:
                is_success = await demon.start_in_range(
                    start=data.start if data.start is not None else await demon.get_node_block_number(),
                    end=data.end if data.end is not None else await demon.get_node_block_number(),
                    addresses=data.addresses
                )
            elif data.list_blocks:
                is_success = await demon.start_in_list(
                    list_blocks=data.list_blocks,
                    addresses=data.addresses
                )
            elif data.addresses:
                is_success = await demon.start_in_list(
                    list_blocks=Getter.get_all_blocks_by_list_addresses(addresses=data.addresses),
                    addresses=data.addresses
                )
            else:
                is_success = True
            logger.error(f"SCRIPT RUN SUCCESSFULLY: {is_success}")
        except Exception as error:
            logger.error(f"ERROR STEP 27: {error}")
            logger.error(f"SCRIPT RUN SUCCESSFULLY: False")
        finally:
            if demon is not None:
                await demon.node.close()


if __name__ == '__main__':
    """TRON DEMON V2"""
    namespace = Parser.create_parser().parse_args(sys.argv[1:])
    if namespace.start or namespace.end or namespace.addresses or namespace.blocks:
        asyncio.run(Parser.run(data=BodyRun(
            start=Utils.correct_parser_data(data=namespace.start, _type=int),
            end=Utils.correct_parser_data(data=namespace.end, _type=int),
            list_blocks=Utils.correct_parser_data(data=namespace.blocks, _type=list),
            addresses=Utils.correct_parser_data(data=namespace.addresses, _type=list)
        )))
    else:
        asyncio.run(await TransactionDemon().run())
