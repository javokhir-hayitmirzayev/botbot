from aiogram import F, Router
from aiogram.filters import StateFilter
from src.utilities import TestStates
from src.sections.admin.handlers import (
    handler_show_tests,
    handler_create_test,
    process_test_name,
    process_test_description,
    process_test_file,
    handler_confirm_delete_test,
    handler_delete_test,
    handler_view_test,
)

test_router = Router()
# callback handlers
test_router.callback_query.register(handler_show_tests, F.data == "test_list")
test_router.callback_query.register(handler_create_test, F.data == "test_create")
test_router.callback_query.register(handler_confirm_delete_test, F.data.startswith("test_delete_confirm_"))
test_router.callback_query.register(handler_delete_test, F.data.startswith("test_delete_execute_"))
test_router.callback_query.register(handler_view_test, F.data.startswith("test_view_"))
# message handlers
test_router.message.register(process_test_name, StateFilter(TestStates.WAITING_FOR_TEST_NAME))
test_router.message.register(process_test_description, StateFilter(TestStates.WAITING_FOR_TEST_DESCRIPTION))
test_router.message.register(process_test_file, StateFilter(TestStates.WAITING_FOR_TEST_FILE))
