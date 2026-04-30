from aiogram.fsm.state import State, StatesGroup


class NewStaffState(StatesGroup):
    role = State()
    user = State()


class SuperAdminState(StatesGroup):
    show_staff_page = State()
    remove_staff_page = State()
