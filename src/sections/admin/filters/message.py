from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import Union

from src.database.intances import user_table
from src.utilities import USER_ROLES

class IsAdminMessageFilter(BaseFilter):
    """Allow only messages from users with ADMIN or SUPREME role."""
    async def __call__(self, message: Message) -> Union[bool, dict]:
        user_id = message.from_user.id
        user = await user_table.get("tg_id = $1", (user_id,))
        if not user:
            return False
        if user["role"] in [USER_ROLES.ADMIN.value, USER_ROLES.SUPREME.value]:
            return True
        return False