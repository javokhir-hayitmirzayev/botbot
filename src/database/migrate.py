from .pool import db
from .schema import ENUM_SQL, INDEXES, TABLES
from src.utilities.logger import logger

async def run_migration():
    try:
        # Initialize the database connection first
        await db.connect()

        logger.info("Starting migration...")

        # 1. Create enums first (SQLite doesn't support enums, but keeping for consistency)
        logger.info("Creating Enums...")
        if ENUM_SQL:
            await db.conn.execute(ENUM_SQL)

        # 2. Create tables
        logger.info("Creating Tables...")
        for table_name, table_sql in TABLES.items():
            logger.info(" - Creating %s...", table_name)
            await db.conn.execute(table_sql)

        # 3. Create indexes
        logger.info("Creating Indexes...")
        for idx_sql in INDEXES:
            await db.conn.execute(idx_sql)

        logger.info("Schema created successfully!")
        return True

    except Exception as e:
        logger.exception("Error during migration: %s", e)
        raise e