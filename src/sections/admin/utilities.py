from src.utilities import USERS_PER_PAGE
from src.database.intances import user_table
from src.utilities.logger import logger
from src.sections.admin.messages import AdminMessages
from src.bot import bot
from src.utilities.types import USER_ROLES


async def get_users_list(page: int = 0):
    offset = page * USERS_PER_PAGE
    users = await user_table.execute(
        "SELECT * FROM users WHERE role = $1 ORDER BY id LIMIT $2 OFFSET $3", (USER_ROLES.ADMIN.value, USERS_PER_PAGE, offset)
    )

    total_users = len(users)

    users_list = []
    for user in users:
        try:
            tg_user = await bot.get_chat(user["tg_id"])
            user_name = tg_user.full_name
            username = f"@{tg_user.username}" if tg_user.username else "No username"
        except Exception as e:
            user_name = "N/A"
            username = "N/A"

        users_list.append(
            f"👤 <b>{user_name}</b>\n"
            f"├─ Role: <code>{user['role']}</code>\n"
            f"└─ Username: {username}\n"
        )

    message_text = (
        f"{AdminMessages.USERS_LIST}\n\n"
        f"📋 Total users: {total_users}\n\n"
        f"{chr(10).join(users_list) if users_list else 'No users found'}"
    )
    return {"message_text": message_text, "users": users, "total_users": total_users}


async def get_user_info(user):
    try:
        created_at = user.get("created_at")
        if created_at:
            created_at = created_at.strftime("%d %b %Y, %H:%M")
        else:
            created_at = "N/A"

        updated_at = user.get("updated_at")
        if updated_at:
            updated_at = updated_at.strftime("%d %b %Y, %H:%M")
        else:
            updated_at = "N/A"

        tg_user = await bot.get_chat(user["tg_id"])
        user_name = tg_user.full_name
        username = f"@{tg_user.username}" if tg_user.username else "No username"

        user_info = (
            "<b>👤 User Details</b>\n\n"
            f"<b>🆔 Name:</b> <code>{user_name}</code>\n"
            f"<b>👤 Username:</b> {username}\n"
            f"<b>👑 Role:</b> <code>{user['role']}</code>\n"
            f"<b>📅 Created At:</b> <code>{created_at}</code>\n"
            f"<b>🔄 Last Updated:</b> <code>{updated_at}</code>"
        )

        if user.get("created_by"):
            creator = await user_table.get("id = $1", (user["created_by"],))
            if creator:
                creator_tg = await bot.get_chat(creator["tg_id"])
                creator_name = creator_tg.full_name
                user_info += f"\n\n<b>👤 Created By:</b> <code>{creator_name} (ID: {creator['id']})</code>"

        return user_info

    except Exception as e:
        logger.exception("Error in get_user_info: %s", e)
        return (
            "<b>👤 User Details</b>\n\n"
            f"<b>🆔 Name:</b> <code>{user.get('first_name', 'N/A')}</code>\n"
            f"<b>👑 Role:</b> <code>{user.get('role', 'N/A')}</code>\n"
            f"<b>📅 Created At:</b> <code>N/A</code>\n"
            f"<b>🔄 Last Updated:</b> <code>N/A</code>"
        )
