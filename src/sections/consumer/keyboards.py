from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.sections.consumer.messages import ConsumerMessages


def get_tests_list_keyboard(tests_with_status: list) -> InlineKeyboardMarkup:
    """Keyboard with list of available tests"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for t in tests_with_status:
        keyboard.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{t['name']}{t['status']}",
                    callback_data=f"start_test_{t['id']}",
                )
            ]
        )

    return keyboard


def get_start_test_keyboard() -> InlineKeyboardMarkup:
    """Keyboard shown before starting a test (single Start button)."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Start Now",
                    callback_data="nav_question_0",
                )
            ]
        ]
    )


def get_question_keyboard(
    question: dict,
    options: list,
    selected_option_ids: list[int],
    current_index: int,
    total_questions: int,
) -> InlineKeyboardMarkup:
    """Keyboard with options + navigation for a question (poll style)."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    # 1. Option buttons with visual state
    for option in options:
        is_selected = option["id"] in selected_option_ids

        if question["type"] == "SINGLE_CHOICE":
            icon = "🔘" if is_selected else "⚪️"
            callback_action = f"select_option_{option['id']}"
        else:  # MULTIPLE_CHOICE
            icon = "☑️" if is_selected else "⬜️"
            callback_action = f"toggle_option_{option['id']}"

        text = f"{icon} {option['label']}) {option['answer']}"

        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text=text, callback_data=callback_action)]
        )

    # 2. Navigation row
    nav_row: list[InlineKeyboardButton] = []

    if current_index > 0:
        nav_row.append(
            InlineKeyboardButton(
                text="⬅️ Prev", callback_data=f"nav_question_{current_index - 1}"
            )
        )
    else:
        nav_row.append(InlineKeyboardButton(text=" ", callback_data="ignore"))

    nav_row.append(
        InlineKeyboardButton(
            text=f"{current_index + 1}/{total_questions}", callback_data="ignore"
        )
    )

    if current_index < total_questions - 1:
        nav_row.append(
            InlineKeyboardButton(
                text="Next ➡️",
                callback_data=f"nav_question_{current_index + 1}",
            )
        )
    else:
        nav_row.append(
            InlineKeyboardButton(text="✅ Submit", callback_data="confirm_submit")
        )

    keyboard.inline_keyboard.append(nav_row)

    # 3. Optional early submit
    if current_index < total_questions - 1:
        keyboard.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="📥 Submit Test Early", callback_data="confirm_submit"
                )
            ]
        )

    return keyboard


def get_confirm_submit_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for confirming test submission."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Yes, Submit All",
                    callback_data="submit_test_final",
                ),
                InlineKeyboardButton(
                    text="🔙 Keep Answering",
                    callback_data="cancel_submit",
                ),
            ]
        ]
    )
