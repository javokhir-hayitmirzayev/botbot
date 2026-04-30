from aiogram import Dispatcher

# Admin panel disabled for referral bot
# from src.sections.supreme.router import supreme_router  # noqa
# from src.sections.admin import admin_router, test_router # noqa
# from src.sections.consumer.router import consumer_router  # noqa
from ..sections.common.routers import start_router


#
#
def register_routers(dp: Dispatcher):
    dp.include_router(start_router)
    # Admin panel disabled for referral bot
    # dp.include_router(supreme_router)
    # dp.include_router(admin_router)
    # dp.include_router(consumer_router)
    # dp.include_router(test_router)
