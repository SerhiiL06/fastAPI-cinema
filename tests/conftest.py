import asyncio

import pytest
from sqlalchemy import Engine
from alembic.command import upgrade, downgrade
from alembic.config import Config as AlembicConfig
from sqlalchemy_utils import database_exists, create_database, drop_database
from src.infrastructure.database.connections import session_transaction
from httpx import ASGITransport, AsyncClient
from .database import session
from sqlalchemy_utils import (
    create_database,
    database_exists,
    drop_database,
)
from .database import test_engine
from src.infrastructure.database.models.base import Base

from main import app
import os
import pathlib


ALEMBIC_CONFIG = pathlib.Path("alembic.ini")


@pytest.fixture(scope="session", autouse=True)
def _migrate(postgres_url_with_template_db: str):
    alembic_cfg = AlembicConfig(ALEMBIC_CONFIG)
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        postgres_url_with_template_db,
    )

    upgrade(alembic_cfg, "head")
    yield
    downgrade(alembic_cfg, "base")


@pytest.fixture(scope="session")
def postgres_template_db():
    return get_env(POSTGRES_TEMPLATE_DB)


@pytest.fixture(scope="session")
def postgres_url_with_template_db(
    postgres_template_db: str,
):
    cfg = load_db_config(db=postgres_template_db)
    return cfg.url


@pytest.fixture(scope="session")
def postgres_url():
    cfg = load_db_config()
    return cfg.url


@pytest.fixture()
def engine(postgres_url):
    return create_engine(postgres_url)


@pytest.fixture()
def connection(engine: Engine, postgres_template_db: str):
    if not database_exists(engine.url):
        create_database(engine.url, template=postgres_template_db)

    with engine.connect() as conn:
        yield conn

    if database_exists(engine.url):
        drop_database(engine.url)


async def test_session():
    async with session() as connect:
        yield connect


app.dependency_overrides[session_transaction] = test_session


@pytest.fixture(autouse=True, scope="module")
async def create_db():
    async with test_engine.begin() as eng:
        await eng.run_sync(Base.metadata.create_all)
        yield
        await eng.run_sync(Base.metadata.drop_all)


@pytest.fixture()
def connection(engine: Engine, postgres_template_db: str):
    if not database_exists(engine.url):
        create_database(engine.url, template=postgres_template_db)

    with engine.connect() as conn:
        yield conn

    if database_exists(engine.url):
        drop_database(engine.url)


@pytest.fixture(scope="session", autouse=True)
def _migrate(postgres_url_with_template_db: str):
    alembic_cfg = AlembicConfig(ALEMBIC_CONFIG)
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        postgres_url_with_template_db,
    )

    upgrade(alembic_cfg, "head")
    yield
    downgrade(alembic_cfg, "base")


@pytest.fixture(scope="session")
async def aclient():
    async with ASGITransport(app=app) as tr:
        aclient = AsyncClient(
            transport=tr,
            base_url="http://test",
        )
        yield aclient
