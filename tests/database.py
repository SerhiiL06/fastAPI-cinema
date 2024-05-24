import os
import pathlib

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from src.infrastructure.database.connections import DatabaseCORE

load_dotenv()


ALEMBIC_CONFIG = pathlib.Path("alembic.ini")


test_core = DatabaseCORE(
    os.getenv("DB_TEST_NAME"),
    os.getenv("DB_TEST_USERNAME"),
    os.getenv("DB_TEST_PASSWORD"),
    os.getenv("D_TEST_HOST"),
    os.getenv("DB_TEST_PORT"),
)
