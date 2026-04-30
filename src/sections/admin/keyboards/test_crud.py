from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_tests_list_keyboard(tests: list) -> InlineKeyboardMarkup:
    """Keyboard listing all tests with create/back options."""
    keyboard = []

    for test in tests:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"📝 {test['name']}", callback_data=f"test_view_{test['id']}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="➕ Create New Test", callback_data="test_create"
            ),
            InlineKeyboardButton(text="🔙 Back", callback_data="admin_menu"),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_test_actions_keyboard(test_id: int) -> InlineKeyboardMarkup:
    """Keyboard with actions for a selected test (back/delete)."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Back to Tests", callback_data="test_list"
                ),
                InlineKeyboardButton(
                    text="🗑️ Delete Test", callback_data=f"test_delete_confirm_{test_id}"
                ),
            ]
        ]
    )


def get_test_creation_success_keyboard() -> InlineKeyboardMarkup:
    """Keyboard shown after successful test creation (view tests / menu)."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👁️ View Tests", callback_data="test_list"),
                InlineKeyboardButton(text="🏠 Main Menu", callback_data="admin_menu"),
            ]
        ]
    )


def get_test_deletion_confirm_keyboard(test_id: int) -> InlineKeyboardMarkup:
    """Keyboard asking to confirm or cancel deletion of a test."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Yes, delete",
                    callback_data=f"test_delete_execute_{test_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Cancel",
                    callback_data="test_list",
                )
            ],
        ]
    )


def get_no_tests_keyboard() -> InlineKeyboardMarkup:
    """Keyboard shown when there are no tests yet (create/back)."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Create Test", callback_data="test_create"
                ),
                InlineKeyboardButton(text="🔙 Back", callback_data="admin_menu"),
            ]
        ]
    )
