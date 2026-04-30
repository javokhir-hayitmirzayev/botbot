from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from src.utilities import _


async def showStaffIKeyboard(page_buttons: list[int]):
    builder = InlineKeyboardBuilder()
    if page_buttons[0] > 0:
        builder.row(
            InlineKeyboardButton(text=_("Back"), callback_data="show_staff_page_back")
        )
    if page_buttons == [1, 1]:
        builder.add(
            InlineKeyboardButton(text=_("Next"), callback_data="show_staff_page_next")
        )
    elif page_buttons[1] > 0:
        builder.row(
            InlineKeyboardButton(text=_("Next"), callback_data="show_staff_page_next")
        )

    return builder.as_markup()
