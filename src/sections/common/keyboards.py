from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_pagination_keyboard(
    current_page: int,
    total_items: int,
    items_per_page: int,
    callback_prefix: str = "users",
) -> InlineKeyboardMarkup:
    """Build a generic pagination keyboard for list views."""

    keyboard = []
    nav_buttons = []

    if current_page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="⬅️ Previous",
                callback_data=f"{callback_prefix}_page_{current_page - 1}_prev",
            )
        )
    if (current_page + 1) * items_per_page < total_items:
        nav_buttons.append(
            InlineKeyboardButton(
                text="Next ➡️",
                callback_data=f"{callback_prefix}_page_{current_page + 1}_next",
            )
        )

    if nav_buttons:
        keyboard.append(nav_buttons)

    keyboard.append(
        [
            InlineKeyboardButton(text="🔙 Back", callback_data="admin_menu"),
            InlineKeyboardButton(
                text="🔄 Refresh", callback_data=f"admin_show_{callback_prefix}"
            ),
        ]
    )
    return keyboard

