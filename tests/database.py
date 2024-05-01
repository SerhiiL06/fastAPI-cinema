from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


DB_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(url=DB_URL)


session = async_sessionmaker(test_engine, class_=AsyncSession)


async def test_session():
    async with session() as connect:
        yield connect
