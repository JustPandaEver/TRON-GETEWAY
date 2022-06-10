import sys
import argparse
import asyncio

from src.helper.utils import Utils
from src.helper.types import BodyRun
from src.demon import TransactionDemon


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
    async def run(data: BodyRun):
        pass



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
