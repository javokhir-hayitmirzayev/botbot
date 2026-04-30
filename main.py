import asyncio
from aiogram import Dispatcher
from src.utilities import logger
from src.dispatcher import start_bot

async def main():
    dp = Dispatcher()
    retry_delay = 5
    retry_count = 0

    while True:
        try:
            await start_bot(dp)
            break
        except Exception:
            retry_count += 1
            logger.warning("%d-retry after %d seconds", retry_count, retry_delay)
            await asyncio.sleep(retry_delay)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.exception("Unexpected error in main: %s", e)
