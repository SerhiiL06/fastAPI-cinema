import os
from contextlib import asynccontextmanager, contextmanager

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

load_dotenv()


class DatabaseCORE:
    __DB_NAME = os.getenv("DB_NAME")
    __DB_USERNAME = os.getenv("DB_USERNAME")
    __DB_PASSWORD = os.getenv("DB_PASSWORD")
    __DB_HOST = os.getenv("DB_HOST")
    __DB_PORT = os.getenv("DB_PORT")

    @property
    def database_env(self) -> dict:
        configurate = {
            "DB_NAME": self.__DB_NAME,
            "DB_USERNAME": self.__DB_USERNAME,
            "DB_PASSWORD": self.__DB_PASSWORD,
            "DB_HOST": self.__DB_HOST,
            "DB_PORT": self.__DB_PORT,
        }
        return configurate

    @property
    def _db_url(self):
        return f"postgresql+asyncpg://{self.__DB_USERNAME}:{self.__DB_PASSWORD}@{self.__DB_HOST}:{self.__DB_PORT}/{self.__DB_NAME}"

    @property
    def _engine(self):
        return create_async_engine(
            self._db_url, echo=True, pool_size=10, max_overflow=5
        )

    @property
    def get_session_connection(self) -> async_sessionmaker:
        return async_sessionmaker(self._engine, class_=AsyncSession, autoflush=False)

    @asynccontextmanager
    async def session_transaction(self):
        async with self.get_session_connection() as conn:
            yield conn

    @asynccontextmanager
    async def session(self):
        connection = self.get_session_connection()
        try:
            yield connection
        finally:
            await connection.close()


core = DatabaseCORE()


async def session():
    connection = core.get_session_connection()
    try:
        yield connection
    finally:
        await connection.close()


async def session_transaction():
    async with core.get_session_connection() as conn:
        yield conn
