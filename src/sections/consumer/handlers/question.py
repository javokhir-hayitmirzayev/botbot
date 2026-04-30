from datetime import datetime
import time

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.database.intances import (
    answer_table,
    attempt_table,
    option_table,
    test_table,
    user_table,
)
from src.sections.consumer.keyboards import (
    get_confirm_submit_keyboard,
    get_question_keyboard,
    get_start_test_keyboard,
)
from src.sections.consumer.messages import ConsumerMessages
from src.sections.consumer.utilities import build_question_context
from .results import show_test_results
from src.utilities import ATTEMPT_STATUS, USER_ROLES
from src.utilities.logger import logger


async def start_test(call: CallbackQuery, state: FSMContext):
    """Start a new test or resume in-progress test"""
    test_id = int(call.data.split("_")[-1])
    test = await test_table.get("id = $1", (test_id,))

    if not test:
        await call.message.edit_text(ConsumerMessages.TEST_NOT_FOUND)
        await call.answer()
        return

    # Ensure user exists
    user = await user_table.get("tg_id = $1", (call.from_user.id,))
    if not user:
        await user_table.create(
            {
                "tg_id": call.from_user.id,
                "role": USER_ROLES.CONSUMER.value,
                "username": call.from_user.username or "",
            }
        )
        user = await user_table.get("tg_id = $1", (call.from_user.id,))

    # Check for existing attempt
    attempt = await attempt_table.get(
        "user_id = $1 AND test_id = $2", (user["id"], test_id)
    )

    if attempt and attempt["status"] == ATTEMPT_STATUS.COMPLETED.value:
        await show_test_results(call, attempt["id"])
        return
    elif attempt and attempt["status"] == ATTEMPT_STATUS.IN_PROGRESS.value:
        await state.update_data(
            attempt_id=attempt["id"],
            test_id=test_id,
            start_time=(
                attempt["started_at"].timestamp()
                if attempt["started_at"]
                else time.time()
            ),
        )
        await show_question(call, state, 0)
        return

    # Create new attempt
    await attempt_table.create(
        {
            "user_id": user["id"],
            "test_id": test_id,
            "started_at": datetime.now(),
            "status": ATTEMPT_STATUS.IN_PROGRESS.value,
        }
    )

    # Fetch ID
    attempt = await attempt_table.get(
        "user_id = $1 AND test_id = $2 AND status = $3",
        (user["id"], test_id, ATTEMPT_STATUS.IN_PROGRESS.value),
    )

    await state.update_data(
        {
            "attempt_id": attempt["id"],
            "current_question": 0,
            "start_time": time.time(),
            "test_id": test_id,
        }
    )
    await call.message.edit_text(
        ConsumerMessages.TEST_STARTED.format(
            test_name=test["name"],
            description=test.get("description", ""),
        )
        + "\n\n"
        + ConsumerMessages.TEST_INSTRUCTIONS,
        reply_markup=get_start_test_keyboard(),
    )
    await call.answer()


async def show_question(
    call: CallbackQuery, state: FSMContext, question_index: int = None
):
    data = await state.get_data()
    test_id = data.get("test_id")
    attempt_id = data.get("attempt_id")

    ctx = await build_question_context(test_id, attempt_id, question_index)

    if ctx is None:
        await call.message.edit_text("This test has no questions.")
        await call.answer()
        return

    question_text = ctx["question_text"]
    current_question = ctx["current_question"]
    options = ctx["options"]
    selected_option_ids = ctx["selected_option_ids"]
    total_questions = ctx["total_questions"]
    question_index = ctx["normalized_index"]

    keyboard = get_question_keyboard(
        question=current_question,
        options=options,
        selected_option_ids=selected_option_ids,
        current_index=question_index,
        total_questions=total_questions,
    )

    await state.update_data(current_question=question_index)

    try:
        if call.message:
            await call.message.edit_text(
                text=question_text, reply_markup=keyboard, parse_mode="HTML"
            )
        else:
            await call.message.answer(
                text=question_text, reply_markup=keyboard, parse_mode="HTML"
            )
    except Exception as e:
        if "message is not modified" not in str(e).lower():
            logger.exception("Error rendering question: %s", e)

    await call.answer()


async def handle_navigation(call: CallbackQuery, state: FSMContext):
    target_index = int(call.data.split("_")[-1])
    await show_question(call, state, target_index)


async def handle_option_selection(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    option_id = int(call.data.split("_")[-1])
    attempt_id = data["attempt_id"]

    option = await option_table.get("id = $1", (option_id,))
    if not option:
        await call.answer("Option not found")
        return

    question_id = option["question_id"]

    await answer_table.delete(
        "attempt_id = $1 AND question_id = $2", (attempt_id, question_id)
    )

    await answer_table.create(
        {
            "attempt_id": attempt_id,
            "question_id": question_id,
            "option_id": option_id,
            "is_correct": option["is_correct"],
            "answered_at": datetime.now(),
        }
    )
    await show_question(call, state)


async def handle_toggle_option(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    option_id = int(call.data.split("_")[-1])
    attempt_id = data["attempt_id"]

    option = await option_table.get("id = $1", (option_id,))
    if not option:
        await call.answer("Option not found")
        return

    question_id = option["question_id"]

    existing = await answer_table.get(
        "attempt_id = $1 AND question_id = $2 AND option_id = $3",
        (attempt_id, question_id, option_id),
    )

    if existing:
        await answer_table.delete("id = $1", (existing["id"],))
    else:
        await answer_table.create(
            {
                "attempt_id": attempt_id,
                "question_id": question_id,
                "option_id": option_id,
                "is_correct": option["is_correct"],
                "answered_at": datetime.now(),
            }
        )
    await show_question(call, state)


async def confirm_submit(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        ConsumerMessages.CONFIRM_SUBMIT,
        reply_markup=get_confirm_submit_keyboard(),
    )
    await call.answer()


async def cancel_submit(call: CallbackQuery, state: FSMContext):
    await show_question(call, state)
