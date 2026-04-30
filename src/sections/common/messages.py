from src.utilities import _


class CommonMessages:
    # START
    not_supreme = _("You are not a super admin. You cannot use this bot.")

    start_consumer_message = _(
        "Welcome to the Super Admin Bot! "
        "You can manage users and their roles from here."
    )
    start_admin_message = _(
        "Welcome to the Admin Bot! " "You can manage users and their roles from here."
    )
    start_supreme_message = _(
        "Welcome to the Super Admin Bot!"
        "You can manage users and their roles from here."
    )

    choose_role = _("Please choose a role:")
    choose_user = _("Please choose a user:")
    user_added = _("User has been added successfully.")
    user_removed = _("User has been removed successfully.")
    no_users_found = _("No users found.")

    # LANG
    language_change_success = _("Language changed successfully!")
    language_change_fail = _("Language change was faliure!")
