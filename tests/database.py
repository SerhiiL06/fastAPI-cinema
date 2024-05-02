from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import os
from dotenv import load_dotenv


load_dotenv()

DB_NAME = os.getenv("DB_TEST_NAME")
DB_USERNAME = os.getenv("DB_TEST_USERNAME")
DB_PASSWORD = os.getenv("DB_TEST_PASSWORD")
DB_HOST = os.getenv("DB_TEST_HOST")
DB_PORT = os.getenv("DB_TEST_PORT")


DB_URL = (
    f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

test_engine = create_async_engine(url=DB_URL, echo=True)


session = async_sessionmaker(test_engine, class_=AsyncSession, autoflush=False)
