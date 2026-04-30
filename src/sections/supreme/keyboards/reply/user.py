from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUser
from src.utilities import _


def chooseUserRKeyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=_("Choose a new user"),
                    request_user=KeyboardButtonRequestUser(request_id=1),
                ),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard
