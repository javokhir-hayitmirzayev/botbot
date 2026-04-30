from aiogram import BaseMiddleware
from aiogram.types import Update

from src.utilities import logger


class ErrorHandlerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        try:
            return await handler(event, data)
        except Exception as e:
            logger.exception(f"Error happened: {e}")
            return None
