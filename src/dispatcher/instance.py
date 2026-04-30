from aiogram import Dispatcher


from src.bot import bot
from src.utilities import logger
from .register_routers import register_routers
from .register_middlewares import register_middlewares
from src.database import run_migration


async def start_bot(dp: Dispatcher):
    try:
        await run_migration()
        # Admin panel disabled for referral bot
        # await init_supreme_user()
        await register_middlewares(dp)
        register_routers(dp)
        logger.info("Starting bot polling...")
        await dp.start_polling(bot, skip_updates=False)
    except Exception as e:
        logger.exception("Polling failed: %s", e)
