# middlewares.py
from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from time import time
from collections import deque


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 10, window: int = 60):
        self.limit = limit
        self.window = window
        self.requests: Dict[int, deque] = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:

        user_id = event.from_user.id

        if user_id not in self.requests:
            self.requests[user_id] = deque()

        now = time()
        while self.requests[user_id] and now - self.requests[user_id][0] > self.window:
            self.requests[user_id].popleft()

        if len(self.requests[user_id]) >= self.limit:
            await event.answer("You're sending messages too fast! Please wait.")
            return

        self.requests[user_id].append(now)

        return await handler(event, data)
