from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import os

load_dotenv()


class DatabaseCORE:
    __DB_NAME = os.getenv("DB_NAME")
    __DB_USERNAME = os.getenv("DB_USERNAME")
    __DB_PASSWORD = os.getenv("DB_PASSWORD")
    __DB_HOST = os.getenv("DB_HOST")
    __DB_PORT = os.getenv("DB_PORT")

    @property
    def _db_url(self):
        return f"postgresql+asyncpg://{self.__DB_USERNAME}:{self.__DB_PASSWORD}@{self.__DB_HOST}:{self.__DB_PORT}/{self.__DB_NAME}"

    @property
    def _engine(self):
        return create_async_engine(self._db_url, echo=True)

    @property
    def get_session_connection(self):
        return async_sessionmaker(self._engine, class_=AsyncSession, autoflush=False)


core = DatabaseCORE()


async def session():
    async with core.get_session_connection() as conn:
        yield conn
