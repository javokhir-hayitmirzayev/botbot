from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.database.intances import user_table
from src.utilities import USERS_PER_PAGE, USER_ROLES
from src.services.delete_user import delete_user_with_relations
from src.sections.admin.keyboards import (
    get_admin_cancel_keyboard,
    get_admin_confirm_keyboard,
    get_admin_main_menu,
    get_user_actions_keyboard,
    get_users_pagination_keyboard,
)
from src.sections.admin.messages import AdminMessages
from src.sections.admin.utilities import get_user_info, get_users_list


##
##
async def handler_admin_menu(call: CallbackQuery):
    """Show the main admin menu with appropriate options."""
    user = await user_table.get("tg_id = $1", (call.from_user.id,))
    is_supreme = user is not None and user["role"] == USER_ROLES.SUPREME.value

    await call.message.edit_text(
        AdminMessages.MAIN_MENU, reply_markup=get_admin_main_menu(is_supreme)
    )
    await call.answer()


async def handler_show_users(call: CallbackQuery, state: FSMContext, page: int = 0):
    """Display paginated list of users for admin management."""
    # Ensure get_users_list is also async in your utilities!
    users_data = await get_users_list(page)
    message_text = users_data["message_text"]
    total_users = users_data["total_users"]
    users = users_data["users"]
    if call.message.text != message_text:
        await call.message.edit_text(
            message_text,
            reply_markup=get_users_pagination_keyboard(
                page, total_users, USERS_PER_PAGE, users
            ),
        )
    await call.answer()


async def handle_users_pagination(call: CallbackQuery, state: FSMContext):
    """Handle next/prev page navigation for the users list."""
    action = call.data.split("_")[-1]
    current_page = (
        int(call.data.split("_")[-2]) if call.data.split("_")[-2].isdigit() else 0
    )

    if action == "prev" and current_page > 0:
        await handler_show_users(call, state, current_page - 1)
    elif action == "next":
        await handler_show_users(call, state, current_page + 1)
    else:
        await call.answer()


async def handler_show_user_details(call: CallbackQuery):
    """Show detailed information and actions for a selected user."""
    user_id = int(call.data.split("_")[-1])
    user = await user_table.get("id = $1", (user_id,))

    if not user:
        await call.answer("❌ User not found", show_alert=True)
        return

    user_info = await get_user_info(user)
    await call.message.edit_text(
        user_info, reply_markup=get_user_actions_keyboard(user["id"])
    )
    await call.answer()


async def handler_delete_user(call: CallbackQuery, state: FSMContext):
    """Handle delete user action by removing the user and related data."""
    user_id = int(call.data.split("_")[-1])
    user = await user_table.get("id = $1", (user_id,))

    if not user:
        await call.answer("❌ User not found", show_alert=True)
        return

    success, error = await delete_user_with_relations(user_id)

    if success:
        # After deletion, show the updated users list again
        await handler_show_users(call, state)
    else:
        await call.message.edit_text(
            f"❌ Error deleting user: {error or 'Unknown error'}"
        )

    await call.answer()


async def handler_manage_content(call: CallbackQuery, state: FSMContext):
    """Open content management menu for the admin panel."""
    await call.message.edit_text(
        AdminMessages.CONTENT_MENU, reply_markup=get_admin_cancel_keyboard()
    )
    await call.answer()


async def handler_show_settings(call: CallbackQuery):
    """Show bot/admin settings menu."""
    await call.message.edit_text(
        AdminMessages.SETTINGS, reply_markup=get_admin_cancel_keyboard()
    )
    await call.answer()


async def handler_confirm_action(call: CallbackQuery, state: FSMContext):
    """Render confirmation dialog based on pending admin action in state."""
    data = await state.get_data()
    action = data.get("action")

    if action == "delete_user":
        user_id = data.get("user_id")
        await call.message.edit_text(
            AdminMessages.CONFIRM_DELETE_USER.format(user_id=user_id),
            reply_markup=get_admin_confirm_keyboard(),
        )

    await call.answer()


async def handler_cancel(call: CallbackQuery, state: FSMContext):
    """Cancel current admin operation and return to main menu."""
    await state.clear()
    user = await user_table.get("tg_id = $1", (call.from_user.id,))
    is_supreme = user is not None and user["role"] == USER_ROLES.SUPREME.value
    await call.message.edit_text(
        AdminMessages.OPERATION_CANCELLED, reply_markup=get_admin_main_menu(is_supreme)
    )
    await call.answer()


async def handler_back(call: CallbackQuery, state: FSMContext):
    """Go back to the admin main menu from nested admin views."""
    await state.clear()
    await handler_admin_menu(call)
