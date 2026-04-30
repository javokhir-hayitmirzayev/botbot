from functools import wraps
from typing import Callable, Any, Coroutine
from .pool import db
from src.utilities.logger import logger

# decorator to handle database connections
def connection(func: Callable[..., Coroutine[Any, Any, Any]]):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if db.conn is None:
            await db.connect()
        conn = db.conn
        try:
            result = await func(self, conn, *args, **kwargs)
            await conn.commit()
            return result
        except Exception as e:
            await conn.rollback()
            logger.exception("Database Error in %s: %s", func.__name__, e)
            raise
    return wrapper