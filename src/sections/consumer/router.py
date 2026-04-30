# /Users/numeodev/Documents/work/dab-base/src/sections/consumer/router.py
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from src.sections.consumer.handlers import (
    show_available_tests,
    start_test,
    handle_option_selection,
    handle_toggle_option,
    confirm_submit,
    handle_navigation,
    cancel_submit,
    submit_test_final
)

# Initialize the router
consumer_router = Router()

consumer_router.callback_query.register(show_available_tests, F.data == "show_available_tests")
consumer_router.callback_query.register(start_test, F.data.startswith("start_test_"))

# Navigation
consumer_router.callback_query.register(handle_navigation, F.data.startswith("nav_question_"))

# Options
consumer_router.callback_query.register(handle_option_selection, F.data.startswith("select_option_"))
consumer_router.callback_query.register(handle_toggle_option, F.data.startswith("toggle_option_"))

# Submission
consumer_router.callback_query.register(confirm_submit, F.data == "confirm_submit")
consumer_router.callback_query.register(cancel_submit, F.data == "cancel_submit")
consumer_router.callback_query.register(submit_test_final, F.data == "submit_test_final")

# Ignore
consumer_router.callback_query.register(lambda c: c.answer(), F.data == "ignore")
