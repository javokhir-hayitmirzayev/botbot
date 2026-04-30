from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.database.intances import user_table
from src.sections.supreme.messages import SuperAdminMessages
from src.sections.supreme.keyboards import showStaffForRemoveIKeyboard
from src.utilities.logger import logger


#
#
#
async def handler_show_staff_for_delete(call: CallbackQuery, state: FSMContext):

    # Updated: Moved LIMIT/OFFSET into the query string and used $1, $2
    # Note: Using OFFSET 1 skips the first record (likely the Supreme Admin or creator)
    staff = await user_table.filter(
        "role = $1 ORDER BY id LIMIT 20 OFFSET $2", ("user", 1)
    )

    if not staff:
        await call.message.edit_text(SuperAdminMessages.no_staff_found)
        return

    await state.update_data(remove_page=1)
    page_buttons = [0, [0, 1][len(staff) > 10]]

    await call.message.edit_text(
        SuperAdminMessages.staff_found,
        reply_markup=showStaffForRemoveIKeyboard(staff[:10], page_buttons),
    )
    await call.answer()


#
#
#
async def handler_remove_staff(call: CallbackQuery, state: FSMContext):

    user_id = int(call.data.replace("delete_staff_", ""))
    try:
        # Updated: await + $1 placeholder
        await user_table.delete("tg_id = $1", (user_id,))
        await call.answer(SuperAdminMessages.staff_deleted_success)

        page = int(await state.get_data().get("remove_page", 1))

        # Updated: Query with pagination in string
        staff = await user_table.filter(
            "role = $1 ORDER BY id LIMIT 20 OFFSET $2", ("user", page)
        )
        page_buttons = [page > 10, len(staff) > 10]

        await call.message.edit_text(
            SuperAdminMessages.staff_found,
            reply_markup=showStaffForRemoveIKeyboard(staff[:10], page_buttons),
        )

    except Exception as e:
        logger.exception("Error removing staff: %s", e)
        await call.answer(SuperAdminMessages.staff_deleted_failure)

    finally:
        # Note: Clearing state here might break pagination if the user wants
        # to delete another one immediately, but keeping original logic.
        await state.clear()


#
#
#
async def handler_remove_staff_turn_page(call: CallbackQuery, state: FSMContext):

    turn = call.data.replace("remove_page_", "")
    # Default to 1 if not found
    current_page_data = await state.get_data()
    page = int(current_page_data.get("remove_page", 1))

    page += [10, -10][turn == "back"]

    # Safety check to prevent negative offset
    if page < 0:
        page = 0

    await state.update_data(remove_page=page)

    # Updated: Query with pagination
    staff = await user_table.filter(
        "role = $1 ORDER BY id LIMIT 20 OFFSET $2", ("user", page)
    )
    page_buttons = [page > 10, len(staff) > 10]

    await call.message.edit_text(
        SuperAdminMessages.staff_found,
        reply_markup=showStaffForRemoveIKeyboard(staff[:10], page_buttons),
    )
    await call.answer()
