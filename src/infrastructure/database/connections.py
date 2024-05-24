import os
from collections.abc import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

load_dotenv()


class DatabaseCORE:
    def __init__(
        self, db_name: str, username: str, password: str, host: str, port: str
    ) -> None:
        self._DB_NAME = db_name
        self._DB_USERNAME = username
        self._DB_PASSWORD = password
        self._DB_HOST = host
        self._DB_PORT = port

    @property
    def database_env(self) -> dict:
        configurate = {
            "DB_NAME": self._DB_NAME,
            "DB_USERNAME": self._DB_USERNAME,
            "DB_PASSWORD": self._DB_PASSWORD,
            "DB_HOST": self._DB_HOST,
            "DB_PORT": self._DB_PORT,
        }
        return configurate

    @property
    def _db_url(self):
        url = URL.create(
            "postgresql+asyncpg",
            self.database_env.get("DB_NAME"),
            self.database_env.get("DB_USERNAME"),
            self.database_env.get("DB_PASSWORD"),
            self.database_env.get("DB_HOST"),
            self.database_env.get("DB_PORT"),
        )
        return url

    @property
    def _engine(self):
        return create_async_engine(
            self._db_url, echo=True, pool_size=10, max_overflow=5
        )

    @property
    def session_factory(self) -> async_sessionmaker:
        return async_sessionmaker(self._engine, class_=AsyncSession, autoflush=False)

    async def session_transaction(self) -> AsyncGenerator:
        async with self.session_factory.begin() as conn:
            yield conn


core = DatabaseCORE(
    os.getenv("POSTGRES_DB"),
    os.getenv("POSTGRES_USERNAME"),
    os.getenv("POSTGRES_PASSWORD"),
    os.getenv("DB_HOST"),
    os.getenv("DB_PORT"),
)


async def session_transaction() -> AsyncGenerator:
    async with core.session_factory() as conn:
        yield conn
