from aiogram import Router, F
from aiogram.filters import Command

from src.sections.common.handlers import (
    handler_start_command,
    handler_link_command,
    handler_link_button,
    handler_rating_command,
    handler_rating_button,
    handler_top_command,
    handler_top_button,
    handler_check_membership_callback,
)

start_router = Router()

# CREATE
start_router.message.register(handler_start_command, Command("start"))
start_router.message.register(handler_link_command, Command("link"))
start_router.message.register(handler_rating_command, Command("reyting"))
start_router.message.register(handler_top_command, Command("top"))

# Button handlers
start_router.message.register(handler_link_button, F.text == "🔗 Havola")
start_router.message.register(handler_rating_button, F.text == "📊 Reyting")
start_router.message.register(handler_top_button, F.text == "🏆 Top")

start_router.callback_query.register(handler_check_membership_callback, F.data == "check_membership")
