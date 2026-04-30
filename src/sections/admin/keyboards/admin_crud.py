from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.sections.common.keyboards import get_pagination_keyboard

def get_admin_main_menu(is_supreme: bool) -> InlineKeyboardMarkup:
    """Build the main admin menu keyboard (with extra options for supreme)."""
    keyboard = []
    if is_supreme:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text="👥 Manage Users", callback_data="admin_show_users"
                )
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(text="➕ Create Test", callback_data="test_create"),
            InlineKeyboardButton(text="📝 Show tests", callback_data="test_list"),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_admin_cancel_keyboard() -> InlineKeyboardMarkup:
    """Keyboard with Back and Main Menu buttons for admin flows."""
    keyboard = [
        [InlineKeyboardButton(text="🔙 Back", callback_data="admin_back")],
        [InlineKeyboardButton(text="🏠 Main Menu", callback_data="admin_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_admin_confirm_keyboard(
    confirm_data: str = "confirm_action",
) -> InlineKeyboardMarkup:
    """Keyboard with Confirm/Cancel buttons for admin confirmations."""
    keyboard = [
        [
            InlineKeyboardButton(
                text="✅ Confirm", callback_data=f"{confirm_data}_yes"
            ),
            InlineKeyboardButton(text="❌ Cancel", callback_data="admin_cancel"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_users_pagination_keyboard(
    current_page: int, total_items: int, items_per_page: int, users: list
) -> InlineKeyboardMarkup:
    """Create pagination keyboard for users list with user buttons."""
    pagination_keyboard = get_pagination_keyboard(
        current_page, total_items, items_per_page, "users"
    )
    users_keyboard = []
    for index, user in enumerate(users):
        users_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{index + 1}", callback_data=f"admin_view_user_{user['id']}"
                )
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=users_keyboard + pagination_keyboard)



def get_user_actions_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Keyboard with actions available for a specific user."""
    keyboard = [
        [
            InlineKeyboardButton(
                text="👀 View Details", callback_data=f"admin_view_user_{user_id}"
            ),
            InlineKeyboardButton(
                text="✏️ Edit", callback_data=f"admin_edit_user_{user_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="❌ Delete", callback_data=f"admin_delete_user_{user_id}"
            ),
        ],
        [
            InlineKeyboardButton(text="🔙 Back", callback_data="admin_show_users"),
            InlineKeyboardButton(text="🏠 Main Menu", callback_data="admin_menu"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_user_actions_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Keyboard with actions available for a specific user."""
    keyboard = [
        [
            InlineKeyboardButton(
                text="👀 View Details", callback_data=f"admin_view_user_{user_id}"
            ),
            InlineKeyboardButton(
                text="❌ Delete", callback_data=f"admin_delete_user_{user_id}"
            ),
        ],
        [
            InlineKeyboardButton(text="🔙 Back", callback_data="admin_show_users"),
            InlineKeyboardButton(text="🏠 Main Menu", callback_data="admin_menu"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
