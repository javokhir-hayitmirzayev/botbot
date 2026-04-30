from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from src.utilities import _


async def showStaffForRemoveIKeyboard(staff: list, page_buttons: list[int]):
    builder = InlineKeyboardBuilder()
    for i in staff:
        builder.row(
            InlineKeyboardButton(
                text=f"{['@' + i['username'], i['first_name']][i['username'] is None]}",
                callback_data=f"delete_staff_{i['tg_id']}",
            )
        )

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
