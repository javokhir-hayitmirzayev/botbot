from aiogram import F, Router
from src.sections.admin.filters import IsAdminMessageFilter, IsAdminCallbackFilter
from src.sections.admin.handlers import (
    handler_show_users,
    handler_admin_menu,
    handler_show_user_details,
    handler_delete_user,
    handler_manage_content,
    handler_show_settings,
    handler_confirm_action,
    handler_cancel,
    handler_back,
    handle_users_pagination,
)

admin_router = Router()

# Apply global filters for all handlers in this router
admin_router.message.filter(IsAdminMessageFilter())
admin_router.callback_query.filter(IsAdminCallbackFilter())

# Callback query handlers
admin_router.callback_query.register(handler_admin_menu, F.data == "admin_menu")
admin_router.callback_query.register(handler_show_users, F.data == "admin_show_users")
admin_router.callback_query.register(
    handler_manage_content, F.data == "admin_manage_content"
)
admin_router.callback_query.register(
    handler_show_settings, F.data == "admin_show_settings"
)
admin_router.callback_query.register(
    handler_confirm_action, F.data.startswith("confirm_")
)
admin_router.callback_query.register(handler_cancel, F.data == "admin_cancel")
admin_router.callback_query.register(handler_back, F.data == "admin_back")

admin_router.callback_query.register(
    handler_show_user_details, F.data.regexp(r"^admin_view_user_(\d+)$")
)

admin_router.callback_query.register(
    handler_delete_user, F.data.regexp(r"^admin_delete_user_(\d+)$")
)

admin_router.callback_query.register(
    handle_users_pagination, F.data.regexp(r"^users_page_(\d+)_(prev|next)$")
)
