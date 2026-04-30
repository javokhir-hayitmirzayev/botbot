from typing import Tuple, Optional

from src.database import db


async def delete_test_with_relations(test_id: int) -> Tuple[bool, Optional[str]]:
    """delete a test and all its related data"""
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                # delete answers linked via option/question/attempt for this test
                await conn.execute(
                    """
                    DELETE FROM answers
                    WHERE option_id IN (
                        SELECT o.id
                        FROM options o
                        JOIN questions q ON q.id = o.question_id
                        WHERE q.test_id = $1
                    )
                    OR question_id IN (
                        SELECT q.id FROM questions q WHERE q.test_id = $1
                    )
                    OR attempt_id IN (
                        SELECT a.id FROM attempts a WHERE a.test_id = $1
                    )
                    """,
                    test_id,
                )

                # delete options for questions
                await conn.execute(
                    """
                    DELETE FROM options
                    WHERE question_id IN (
                        SELECT id FROM questions WHERE test_id = $1
                    )
                    """,
                    test_id,
                )

                # delete questions for this test
                await conn.execute(
                    "DELETE FROM questions WHERE test_id = $1",
                    test_id,
                )

                # delete attempts for this test
                await conn.execute(
                    "DELETE FROM attempts WHERE test_id = $1",
                    test_id,
                )

                # delete the test
                await conn.execute(
                    "DELETE FROM tests WHERE id = $1",
                    test_id,
                )

        return True, None
    except Exception as e:
        return False, str(e)
