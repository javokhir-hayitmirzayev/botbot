from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from typing import Union

from src.database.intances import user_table  # noqa
from src.utilities import USER_ROLES


class IsSuperAdminCallbackFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> Union[bool, dict]:
        user_id = callback.from_user.id
        user = await user_table.get("tg_id = $1", (user_id,))
        if not user:
            return False

        if user["role"] == USER_ROLES.SUPREME.value:
            return True

        return False