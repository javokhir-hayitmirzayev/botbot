from typing import Tuple, Optional

from src.database import db


async def delete_user_with_relations(user_id: int) -> Tuple[bool, Optional[str]]:
    """delete a user and all related data"""
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                # remove the attempt answers
                await conn.execute(
                    """
                    DELETE FROM answers
                    WHERE attempt_id IN (
                        SELECT id FROM attempts WHERE user_id = $1
                    )
                    """,
                    user_id,
                )

                # remove the atempts
                await conn.execute(
                    "DELETE FROM attempts WHERE user_id = $1",
                    user_id,
                )

                # remove the user
                await conn.execute(
                    "DELETE FROM users WHERE id = $1",
                    user_id,
                )

        return True, None
    except Exception as e:
        return False, str(e)
