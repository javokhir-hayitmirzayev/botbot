from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from src.utilities.env import env

bot = Bot(
    token=env("BOT_TOKEN"),
    default=DefaultBotProperties(parse_mode="HTML"),
)
