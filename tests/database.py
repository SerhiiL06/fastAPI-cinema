import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv()


class TestDataBaseCore:

    DB_NAME = os.getenv("DB_TEST_NAME")
    DB_USERNAME = os.getenv("DB_TEST_USERNAME")
    DB_PASSWORD = os.getenv("DB_TEST_PASSWORD")
    DB_HOST = os.getenv("DB_TEST_HOST")
    DB_PORT = os.getenv("DB_TEST_PORT")

    def test_db_url_template(self):
        return f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/template_db"

    def test_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def test_engine(self):
        return create_async_engine(url=self.test_db_url(), echo=True)

    @property
    def test_session(self):
        return async_sessionmaker(self.test_engine, class_=AsyncSession)

    async def test_connection(self):
        async with self.test_session() as conn:
            yield conn


test_core = TestDataBaseCore()
