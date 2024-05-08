from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)


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
        return f"postgresql+asyncpg://{self._DB_USERNAME}:{self._DB_PASSWORD}@{self._DB_HOST}:{self._DB_PORT}/{self._DB_NAME}"

    @property
    def _engine(self):
        return create_async_engine(self._db_url, pool_size=10, max_overflow=5)

    @property
    def session_factory(self) -> async_sessionmaker:
        return async_sessionmaker(self._engine, class_=AsyncSession, autoflush=False)

    @property
    async def session_transaction(self) -> AsyncGenerator:
        async with self.session_factory() as conn:
            yield conn

    @asynccontextmanager
    async def session(self) -> AsyncGenerator:
        connection = self.get_session_connection()
        try:
            yield connection
        finally:
            await connection.close()
