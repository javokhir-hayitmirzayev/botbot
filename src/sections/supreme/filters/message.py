from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import Union

from src.database.intances import user_table  # noqa
from src.utilities import USER_ROLES

class IsSuperAdminMessageFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, dict]:
        user_id = message.from_user.id
        user = await user_table.get("tg_id = $1", (user_id,))
        if not user:
            return False
            
        if user["role"] == USER_ROLES.SUPREME.value:
            return True

        return False