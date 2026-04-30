import aiosqlite
from src.utilities.env import env

class Database:
    def __init__(self):
        self.conn: aiosqlite.Connection = None

    async def connect(self):
        if self.conn is None:
            db_path = env("DB_PATH", "bot.db")
            self.conn = await aiosqlite.connect(db_path)
            self.conn.row_factory = aiosqlite.Row
        return self.conn

    async def disconnect(self):
        if self.conn:
            await self.conn.close()
            self.conn = None

    async def get_conn(self):
        if not self.conn:
            await self.connect()
        return self.conn

db = Database()