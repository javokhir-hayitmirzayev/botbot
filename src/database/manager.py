from src.database.connection import connection

class DBManager:
    def __init__(self, table_name: str):
        self.table_name = table_name

    # CREATE
    @connection
    async def create(self, conn, data: dict):
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in range(len(data)))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        await conn.execute(query, tuple(data.values()))
        return conn.lastrowid

    # READ (One)
    @connection
    async def get(self, conn, condition: str, params: tuple = ()):
        query = f"SELECT * FROM {self.table_name} WHERE {condition}"
        cursor = await conn.execute(query, params)
        row = await cursor.fetchone()
        await cursor.close()
        return dict(row) if row else None

    # ALL
    @connection
    async def all(self, conn):
        query = f"SELECT * FROM {self.table_name}"
        cursor = await conn.execute(query)
        rows = await cursor.fetchall()
        await cursor.close()
        return [dict(row) for row in rows]

    # FILTER
    @connection
    async def filter(self, conn, condition: str, params: tuple = ()):
        query = f"SELECT * FROM {self.table_name} WHERE {condition}"
        cursor = await conn.execute(query, params)
        rows = await cursor.fetchall()
        await cursor.close()
        return [dict(row) for row in rows]

    # ORDER BY
    @connection
    async def order_by(self, conn, order_by: str, order: str = "ASC"):
        if order.upper() not in ("ASC", "DESC"):
            raise ValueError("Invalid order type. Use 'ASC' or 'DESC'.")
        query = f"SELECT * FROM {self.table_name} ORDER BY {order_by} {order}"
        cursor = await conn.execute(query)
        rows = await cursor.fetchall()
        await cursor.close()
        return [dict(row) for row in rows]

    # UPDATE
    @connection
    async def update(self, conn, data: dict, condition: str, params: tuple = ()):
        set_parts = []
        values = []

        for key, value in data.items():
            set_parts.append(f"{key} = ?")
            values.append(value)

        set_clause = ", ".join(set_parts)
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {condition}"
        all_params = tuple(values) + params
        await conn.execute(query, all_params)
        return conn.total_changes


    # DELETE
    @connection
    async def delete(self, conn, condition: str, params: tuple = ()):
        query = f"DELETE FROM {self.table_name} WHERE {condition}"
        await conn.execute(query, params)
        return conn.total_changes

    # COUNT
    @connection
    async def count(self, conn):
        query = f"SELECT COUNT(*) FROM {self.table_name}"
        cursor = await conn.execute(query)
        row = await cursor.fetchone()
        await cursor.close()
        return row[0] if row else 0

    # EXISTS
    @connection
    async def exists(self, conn, condition: str, params: tuple = ()):
        query = f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE {condition})"
        cursor = await conn.execute(query, params)
        row = await cursor.fetchone()
        await cursor.close()
        return bool(row[0]) if row else False

    # EXECUTE
    @connection
    async def execute(self, conn, query: str, params: tuple = ()):
        if query.strip().upper().startswith("SELECT"):
            cursor = await conn.execute(query, params)
            rows = await cursor.fetchall()
            await cursor.close()
            return [dict(row) for row in rows]
        else:
            await conn.execute(query, params)
            return conn.total_changes

    # ---------- Referral Bot Specific Methods ----------

    @connection
    async def add_user(self, conn, user_id: int, referrer_id: int = None, username: str = None, first_name: str = None):
        query = f"INSERT OR IGNORE INTO {self.table_name} (user_id, referrer_id, username, first_name) VALUES (?, ?, ?, ?)"
        cursor = await conn.execute(query, (user_id, referrer_id, username, first_name))
        await cursor.close()
        return cursor.lastrowid

    @connection
    async def is_user_exists(self, conn, user_id: int):
        query = f"SELECT 1 FROM {self.table_name} WHERE user_id = ?"
        cursor = await conn.execute(query, (user_id,))
        row = await cursor.fetchone()
        await cursor.close()
        return row is not None

    @connection
    async def get_invite_count(self, conn, user_id: int):
        query = f"SELECT COUNT(*) FROM {self.table_name} WHERE referrer_id = ? AND user_id != referrer_id"
        cursor = await conn.execute(query, (user_id,))
        row = await cursor.fetchone()
        await cursor.close()
        return row[0] if row else 0

    @connection
    async def get_top_referrers(self, conn, limit: int = 10):
        query = f"""
            SELECT referrer_id, username, COUNT(*) as invite_count
            FROM {self.table_name}
            WHERE referrer_id IS NOT NULL AND user_id != referrer_id
            GROUP BY referrer_id
            ORDER BY invite_count DESC
            LIMIT ?
        """
        cursor = await conn.execute(query, (limit,))
        rows = await cursor.fetchall()
        await cursor.close()
        return [dict(row) for row in rows]

    @connection
    async def get_referrer_of_user(self, conn, user_id: int):
        query = f"SELECT referrer_id FROM {self.table_name} WHERE user_id = ?"
        cursor = await conn.execute(query, (user_id,))
        row = await cursor.fetchone()
        await cursor.close()
        return row[0] if row else None

    @connection
    async def get_username_by_id(self, conn, user_id: int):
        query = f"SELECT username FROM {self.table_name} WHERE user_id = ?"
        cursor = await conn.execute(query, (user_id,))
        row = await cursor.fetchone()
        await cursor.close()
        return row["username"] if row else None

    @connection
    async def get_user_display_name(self, conn, user_id: int):
        query = f"SELECT first_name, username FROM {self.table_name} WHERE user_id = ?"
        cursor = await conn.execute(query, (user_id,))
        row = await cursor.fetchone()
        await cursor.close()
        if not row:
            return f"User {user_id}"
        first_name = row["first_name"]
        username = row["username"]
        if first_name and username:
            return f"{first_name} (@{username})"
        elif first_name:
            return first_name
        elif username:
            return f"@{username}"
        return f"User {user_id}"

    # ---------- Pending Referrals Methods ----------

    @connection
    async def add_pending_referral(self, conn, user_id: int, referrer_id: int, username: str = None, first_name: str = None):
        query = f"INSERT OR REPLACE INTO {self.table_name} (user_id, referrer_id, username, first_name) VALUES (?, ?, ?, ?)"
        cursor = await conn.execute(query, (user_id, referrer_id, username, first_name))
        await cursor.close()
        return cursor.lastrowid

    @connection
    async def get_pending_referral(self, conn, user_id: int):
        query = f"SELECT * FROM {self.table_name} WHERE user_id = ?"
        cursor = await conn.execute(query, (user_id,))
        row = await cursor.fetchone()
        await cursor.close()
        return dict(row) if row else None

    @connection
    async def delete_pending_referral(self, conn, user_id: int):
        query = f"DELETE FROM {self.table_name} WHERE user_id = ?"
        await conn.execute(query, (user_id,))
        return conn.total_changes

    @connection
    async def get_user_rank(self, conn, user_id: int):
        """Get user's rank based on invite count. Higher invites = better rank (lower number)."""
        # Get user's invite count
        query = f"SELECT COUNT(*) as invite_count FROM {self.table_name} WHERE referrer_id = ?"
        cursor = await conn.execute(query, (user_id,))
        row = await cursor.fetchone()
        await cursor.close()
        user_invites = row[0] if row else 0

        # Count users with more invites than this user
        query = f"""
            SELECT COUNT(DISTINCT referrer_id) as count
            FROM {self.table_name}
            WHERE referrer_id IS NOT NULL
            AND referrer_id != ?
            GROUP BY referrer_id
            HAVING COUNT(*) > ?
        """
        cursor = await conn.execute(query, (user_id, user_invites))
        row = await cursor.fetchone()
        await cursor.close()
        users_with_more_invites = row[0] if row else 0

        # Rank = users with more invites + 1
        return users_with_more_invites + 1