from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    """Admin FSM states"""
    # User management states
    waiting_for_user_selection = State()
    waiting_for_user_edit = State()
    waiting_for_user_delete_confirmation = State()
    
    # Content management states
    waiting_for_content_type = State()
    waiting_for_content_edit = State()
    waiting_for_content_creation = State()
    
    # Settings states
    waiting_for_setting_selection = State()
    waiting_for_setting_value = State()

    # Common states
    processing = State() 
    confirmation = State() 

