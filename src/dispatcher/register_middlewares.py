from aiogram import Dispatcher

from .middlewares.error_handler import ErrorHandlerMiddleware
from .middlewares.membership_gate import MembershipGateMiddleware


async def register_middlewares(dp: Dispatcher):
    dp.update.middleware(ErrorHandlerMiddleware())
    dp.update.middleware(MembershipGateMiddleware())
