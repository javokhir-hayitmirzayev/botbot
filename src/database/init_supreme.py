import asyncio

from src.database.pool import db
from src.utilities.env import env
from src.utilities.logger import logger
from src.utilities.types import USER_ROLES


async def init_supreme_user() -> None:
    """Create the initial SUPREME user based on SUPREME_TG_ID from the environment."""

    supreme_tg_id = env("SUPREME_TG_ID", None)
    if not supreme_tg_id:
        logger.warning("SUPREME_TG_ID is not set in environment; skipping supreme user init.")
        return

    try:
        # Ensure the pool is ready
        await db.connect()

        async with db.pool.acquire() as conn:
            # Check if a SUPREME user with this tg_id already exists
            existing = await conn.fetchrow(
                "SELECT id FROM users WHERE tg_id = $1 AND role = $2",
                int(supreme_tg_id),
                USER_ROLES.SUPREME.value,
            )

            if existing:
                logger.info(
                    "SUPREME user already exists with tg_id=%s (id=%s)",
                    supreme_tg_id,
                    existing["id"],
                )
                return

            # Insert a minimal SUPREME user record
            await conn.execute(
                "INSERT INTO users (tg_id, role) VALUES ($1, $2)",
                int(supreme_tg_id),
                USER_ROLES.SUPREME.value,
            )

            logger.info("Created initial SUPREME user with tg_id=%s", supreme_tg_id)

    except Exception as e:
        logger.exception("Error while initializing SUPREME user: %s", e)
