from src.utilities import _


class SuperAdminMessages:
    choose_role = _("Choose a role to countinue:")
    choose_user = _("Choose a user to continue:")
    user_added_success = _("User %s with role %s has been added successfully!")
    user_added_faliure = _(
        "An error occurred while adding the user. Please try again later."
    )

    no_staff_found = _("No staff found. Please add staff first!")
    staff_found = _("Here is the list of staff:\n\n")
    staff_found_empty = _("No staff found. Please add staff first!")
    remove_staff = _("Are you sure you want to remove this staff?")
    staff_deleted_success = _("Staff has been deleted successfully!")
    staff_deleted_failure = _(
        "An error occurred while deleting the staff. Please try again later."
    )
    staff_not_found = _("Staff not found. Please try again.")
    staff_found_for_remove = _("Here is the list of staff:\n\n")
    staff_found_for_remove_empty = _("No staff found. Please add staff first!")
