from aiogram import F  # noqa
from aiogram.fsm.context import FSMContext
from aiogram.types import (  # noqa
    Message,
    CallbackQuery,
    ReplyKeyboardRemove,
)

from src.database.intances import user_table  # noqa
from src.sections.supreme.states import NewStaffState  # noqa
from src.sections.supreme.messages import SuperAdminMessages  # noqa
from src.sections.supreme.keyboards import chooseUserRKeyboard  # noqa
from src.utilities.logger import logger


#
#
#
async def handler_role_chosen(call: CallbackQuery, state: FSMContext):

    await state.update_data(role=call.data.replace("role_", ""))
    await state.set_state(NewStaffState.user)

    await call.message.edit_text(
        SuperAdminMessages.choose_user, reply_markup=chooseUserRKeyboard()
    )
    await call.answer()


#
#
#
async def handler_user_chosen(msg: Message, state: FSMContext):

    state_data = await state.get_data()
    role = state_data.get("role")
    new_user_tid = msg.user_shared.user_id

    try:
        # Updated: await the create method
        await user_table.create({
            "tg_id": new_user_tid,
            "role": role,
            "created_by": msg.from_user.id
        })
        await msg.answer(
            SuperAdminMessages.user_added_success % (msg.from_user.first_name, role),
            reply_markup=ReplyKeyboardRemove(),
        )

    except Exception as e:
        logger.exception("Error creating user: %s", e)
        await msg.answer(
            SuperAdminMessages.user_added_faliure,
            reply_markup=ReplyKeyboardRemove(),
        )

    finally:
        await state.clear()