class AdminMessages:
    # Main menu
    MAIN_MENU = (
        "👨‍💻 *Admin Panel*\n\n"
        "Welcome to the admin panel. Please select an option:"
    )
    
    # User management
    USERS_LIST = "👥 *Users List*\n\nHere are the registered users:"
    USER_DETAILS = "👤 *User Details*\n\nUser ID: `{user_id}`"
    CONFIRM_DELETE_USER = "⚠️ *Confirm Deletion*\n\nAre you sure you want to delete user `{user_id}`?"
    
    # Content management
    CONTENT_MENU = "📝 *Content Management*\n\nManage your bot's content here."
    
    # Settings
    SETTINGS = "⚙️ *Settings*\n\nConfigure bot settings here."
    
    # Common
    OPERATION_CANCELLED = "❌ Operation cancelled."
    SUCCESS = "✅ Operation completed successfully!"
    ERROR = "❌ An error occurred. Please try again later."
    ACCESS_DENIED = "⛔ You don't have permission to perform this action."