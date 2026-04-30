from aiogram import F  # noqa
from aiogram import Router  # noqa
from aiogram.filters import Command  # noqa

#
#
#
from src.sections.supreme.filters import (
    IsSuperAdminMessageFilter,
    IsSuperAdminCallbackFilter,
)

#
#
#
from src.sections.supreme.handlers import (  # noqa
    # CREATE
    handler_role_chosen,
    handler_user_chosen,
    # READ
    handler_show_staff,
    handler_show_staff_turn_page,
    # DELETE
    handler_show_staff_for_delete,
    handler_remove_staff,
    handler_remove_staff_turn_page,
)

#
#
#
supreme_router = Router()

#
#
#
supreme_router.message.filter(IsSuperAdminMessageFilter())
supreme_router.callback_query.filter(IsSuperAdminCallbackFilter())

#
#
# CREATE
supreme_router.callback_query.register(handler_role_chosen, F.data == "role_chosen")
supreme_router.callback_query.register(handler_user_chosen, F.data == "user_chosen")

#
#
# READ
supreme_router.callback_query.register(handler_show_staff, F.data == "show_staff")
supreme_router.callback_query.register(
    handler_show_staff_turn_page, F.data == "show_staff_turn_page"
)

#
#
# DELETE
supreme_router.callback_query.register(
    handler_show_staff_for_delete, F.data == "show_staff_for_delete"
)
supreme_router.callback_query.register(
    handler_remove_staff, F.data == "remove_staff"
)
supreme_router.callback_query.register(
    handler_remove_staff_turn_page, F.data == "remove_staff_turn_page"
)
