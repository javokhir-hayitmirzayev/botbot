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
from src.sections.supreme.keyboards import showStaffIKeyboard  # noqa


#
#
#
async def handler_show_staff(msg: Message, state: FSMContext):

    # Updated: Moved LIMIT/OFFSET into SQL string
    staff = await user_table.filter(
        "role = $1 ORDER BY id LIMIT 20 OFFSET $2", 
        ("user", 1)
    )
    
    if not staff:
        await msg.answer(SuperAdminMessages.no_staff_found)
        return

    await state.update_data(show_page=1)
    page_buttons = [0, [0, 1][len(staff) > 10]]
    
    staff_list = "\n".join(
        [
            f"<b>{j}.</b>{['@' + (i['username'] or ''), i.get('first_name', '')][i.get('username') is None]} - {i['role']}"
            for j, i in enumerate(staff[:10])
        ]
    )
    await msg.answer(
        SuperAdminMessages.staff_found + staff_list,
        reply_markup=showStaffIKeyboard(page_buttons),
    )


#
#
#
async def handler_show_staff_turn_page(call: CallbackQuery, state: FSMContext):

    turn = call.data.replace("page_", "")
    
    current_page_data = await state.get_data()
    page = int(current_page_data.get("show_page", 1))
    
    page += [10, -10][turn == "back"]
    if page < 0: page = 0
    
    await state.update_data(show_page=page)

    # Updated: Query with pagination
    staff = await user_table.filter(
        "role = $1 ORDER BY id LIMIT 20 OFFSET $2", 
        ("user", page)
    )

    if not staff:
        await call.answer(SuperAdminMessages.no_staff_found)
        return

    page_buttons = [page > 10, len(staff) > 10]
    
    # Safe username access using .get
    staff_list = "\n".join(
        [
            f"<b>{j}.</b>{['@' + (i['username'] or ''), i.get('first_name', '')][i.get('username') is None]} - {i['role']}"
            for j, i in enumerate(staff[:10])
        ]
    )
    await call.message.edit_text(
        SuperAdminMessages.staff_found + staff_list,
        reply_markup=showStaffIKeyboard(page_buttons),
    )