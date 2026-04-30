from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.sections.consumer.keyboards import get_tests_list_keyboard
from src.sections.consumer.messages import ConsumerMessages
from src.sections.consumer.utilities import get_all_tests



async def show_available_tests(call: CallbackQuery, state: FSMContext):
    tests_with_status = await get_all_tests(user_id=call.from_user.id)

    if not tests_with_status:
        await call.message.edit_text(ConsumerMessages.NO_TESTS_AVAILABLE)
        await call.answer()
        return

    keyboard = get_tests_list_keyboard(tests_with_status)

    await call.message.edit_text(
        ConsumerMessages.TEST_SELECTION, reply_markup=keyboard
    )
    await call.answer()

