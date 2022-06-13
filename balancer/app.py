import asyncio

from src.runner import run
from config import logger


async def main(loop):
    await asyncio.gather(*[run(loop)])


if __name__ == '__main__':
    loop = None
    try:
        logger.error("START BALANCER")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(loop))
        loop.close()
    except Exception as error:
        logger.error(f"ERROR: {error}")
    finally:
        logger.error("STOP BALANCER")
        if loop is not None and not loop.is_closed():
            loop.close()
