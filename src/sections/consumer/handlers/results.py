from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery

from src.database.intances import attempt_table, test_table
from src.sections.consumer.utilities import finalize_attempt_and_generate_report
from src.services import generate_test_report


async def submit_test_final(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    attempt_id = data.get("attempt_id")
    test_id = data.get("test_id")

    if not attempt_id or not test_id:
        await call.message.edit_text("Session expired. Please restart.")
        await call.answer()
        return

    start_time = data.get("start_time")

    result_text, excel_file, test = await finalize_attempt_and_generate_report(
        attempt_id=attempt_id,
        test_id=test_id,
        start_time=start_time,
    )

    await call.message.edit_text(result_text)
    await call.bot.send_chat_action(
        chat_id=call.message.chat.id, action="upload_document"
    )

    if excel_file:
        filename = f"{test['name'].replace(' ', '_')}_Result.xlsx"
        input_file = BufferedInputFile(excel_file.read(), filename=filename)

        await call.message.answer_document(
            document=input_file, caption="📊 <b>Here is your detailed result.</b>"
        )
    else:
        await call.message.answer("⚠️ Could not generate detailed report.")

    await state.clear()


async def show_test_results(call: CallbackQuery, attempt_id: int):
    attempt = await attempt_table.get("id = $1", (attempt_id,))
    if not attempt:
        await call.answer("Not found")
        return

    test = await test_table.get("id = $1", (attempt["test_id"],))
    if attempt["finished_at"] and attempt["started_at"]:
        duration = attempt["finished_at"] - attempt["started_at"]
        time_str = str(duration).split(".")[0]
    else:
        time_str = "N/A"

    await call.message.edit_text(
        f"🏁 <b>Test Results: {test['name']}</b>\n"
        f"📊 Score: {attempt['score']}%\n"
        f"⏱ Time: {time_str}"
    )

    # Also send the detailed Excel report, similar to submit_test_final
    await call.bot.send_chat_action(
        chat_id=call.message.chat.id, action="upload_document"
    )

    excel_file = await generate_test_report(attempt_id)
    if excel_file:
        filename = f"{test['name'].replace(' ', '_')}_Result.xlsx"
        input_file = BufferedInputFile(excel_file.read(), filename=filename)

        await call.message.answer_document(
            document=input_file,
            caption="📊 <b>Here is your detailed result.</b>",
        )
    else:
        await call.message.answer("⚠️ Could not generate detailed report.")

    await call.answer()
