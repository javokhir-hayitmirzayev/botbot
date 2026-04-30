from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from pathlib import Path
from io import BytesIO

from src.sections.admin.keyboards import (
    get_admin_cancel_keyboard,
    get_tests_list_keyboard,
    get_no_tests_keyboard,
    get_test_creation_success_keyboard,
    get_test_deletion_confirm_keyboard,
    get_test_actions_keyboard
)

from src.database.intances import test_table, question_table, option_table
from src.utilities import TestStates
from src.sections.admin.keyboards import (
    get_admin_cancel_keyboard,
    get_tests_list_keyboard,
)
from src.services.extractor import extract_questions
from src.services.create_test import save_test_data
from src.services import delete_test_with_relations


# Test Management Handlers
async def handler_show_tests(call: CallbackQuery, state: FSMContext):
    """Show list of tests in the admin panel."""
    tests = await test_table.all()

    if not tests:
        # No tests: we can safely reuse the previous message
        await call.message.edit_text(
            "No tests found. Would you like to create one?",
            reply_markup=get_no_tests_keyboard(),
        )
        await call.answer()
        return

    keyboard = get_tests_list_keyboard(tests)
    await call.message.edit_text("📝 Available Tests:", reply_markup=keyboard)
    await call.answer()


async def handler_create_test(call: CallbackQuery, state: FSMContext):
    """Start the test creation flow and ask for test name."""
    await state.set_state(TestStates.WAITING_FOR_TEST_NAME)
    await call.message.edit_text(
        "✏️ Enter the test name:", reply_markup=get_admin_cancel_keyboard()
    )
    await call.answer()

async def process_test_name(message: Message, state: FSMContext):
    """Process test name and ask for description"""
    test_name = message.text.strip()
    await state.update_data(test_name=test_name)
    await state.set_state(TestStates.WAITING_FOR_TEST_DESCRIPTION)
    await message.answer(
        "📝 Enter test description:", reply_markup=get_admin_cancel_keyboard()
    )


async def process_test_description(message: Message, state: FSMContext):
    """Process test description and ask for Excel file"""
    test_description = message.text.strip()
    await state.update_data(test_description=test_description)
    await state.set_state(TestStates.WAITING_FOR_TEST_FILE)
    await message.answer(
        "📤 Please upload an Excel file with test questions.\n\n"
        "File should have these columns:\n"
        "- questions: The question text\n"
        "- A, B, C, D, E: Answer options\n"
        "- answer: Correct answer(s) as comma-separated letters (e.g., 'A' or 'A,C')",
        reply_markup=get_admin_cancel_keyboard(),
    )


async def process_test_file(message: Message, state: FSMContext):
    """Process uploaded Excel file and create the test with questions."""
    if not message.document:
        await message.answer("Please upload an Excel file (.xlsx)")
        return

    if not message.document.file_name.endswith((".xlsx", ".xls")):
        await message.answer("Please upload a valid Excel file (.xlsx or .xls)")
        return

    try:
        # Get file from Telegram
        file = await message.bot.get_file(message.document.file_id)
        file_bytes = await message.bot.download_file(file.file_path)
        excel_data = BytesIO(file_bytes.getvalue())

        # Extract questions from Excel
        questions_data = extract_questions(excel_data)

        if not questions_data:
            await message.answer("❌ No valid questions found in the file.")
            return

        data = await state.get_data()
        test_details = {
            "name": data["test_name"],
            "description": data.get("test_description", ""),
        }

        success, error = await save_test_data(test_details, questions_data)

        if success:
            await message.answer(
                "✅ Test created successfully with Excel import!",
                reply_markup=get_test_creation_success_keyboard(),
            )
        else:
            await message.answer(
                f"❌ Error creating test: {error}",
                reply_markup=get_admin_cancel_keyboard(),
            )

    except Exception as e:
        await message.answer(f"❌ Error processing file: {str(e)}")
        return

    await state.clear()


async def handler_confirm_delete_test(call: CallbackQuery, state: FSMContext):
    """Show confirmation dialog for test deletion"""
    try:
        test_id = int(call.data.split('_')[-1])
        test = await test_table.get("id = $1", (test_id,))

        if not test:
            await call.message.edit_text("❌ Test not found.")
            await call.answer()
            return

        await call.message.edit_text(
            f"⚠️ Are you sure you want to delete the test '{test['name']}'?\n"
            "This will delete all related questions and answers!",
            reply_markup=get_test_deletion_confirm_keyboard(test_id),
        )
        await call.answer()
    except Exception as e:
        await call.answer("❌ An error occurred while processing your request.")

async def handler_delete_test(call: CallbackQuery, state: FSMContext):
    """Delete test and all related data"""
    try:
        test_id = int(call.data.split('_')[-1])
        
        success, error = await delete_test_with_relations(test_id)

        if success:
            await call.message.edit_text(
                "✅ Test and all its questions have been deleted."
            )
            await handler_show_tests(call, state)
        else:
            await call.message.edit_text(
                f"❌ Error deleting test: {error or 'Unknown error'}"
            )
            await call.answer()
        
    except Exception as e:
        await call.message.edit_text(f"❌ Error deleting test: {str(e)}")
        await call.answer()
    finally:
        await state.clear()

async def handler_view_test(call: CallbackQuery, state: FSMContext):
    """View test details"""
    test_id = int(call.data.split("_")[-1])
    test = await test_table.get("id = $1", (test_id,))

    if not test:
        await call.message.edit_text("❌ Test not found.")
        await call.answer()
        return

    questions = await question_table.filter("test_id = $1", (test_id,))
    questions_count = len(questions)

    await call.message.edit_text(
        f"📝 Test: {test['name']}\n"
        f"📋 Description: {test['description']}\n"
        f"❓ Questions: {questions_count}\n\n"
        "What would you like to do?",
        reply_markup=get_test_actions_keyboard(test_id),
    )
    await call.answer()
