import os
import pathlib

import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig
from httpx import ASGITransport, AsyncClient
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import ProgrammingError

from main import app
from src.infrastructure.database.connections import session_transaction

from .database import test_core

ALEMBIC_CONFIG = pathlib.Path("alembic.ini")


@pytest.fixture(scope="session", autouse=True)
def _migrate():

    alembic_cfg = AlembicConfig(ALEMBIC_CONFIG)
    alembic_cfg.set_main_option("sqlalchemy.url", test_core.test_db_url_template())

    upgrade(alembic_cfg, "head")
    yield
    downgrade(alembic_cfg, "base")


@pytest.fixture(scope="session")
def postgres_template_db():
    return test_core.test_db_url_template()


@pytest.fixture(autouse=True)
def engine(postgres_template_db):
    return create_engine(postgres_template_db)


@pytest.fixture(autouse=True)
async def connection(engine: Engine, postgres_template_db: str):

    engine = engine.execution_options(isolation_level="AUTOCOMMIT")

    with engine.connect() as conn:
        try:
            conn.execute(text("CREATE DATABASE cinema_db_test TEMPLATE template_db"))
        except ProgrammingError as e:
            print(e)
        yield
        conn.execute(text("DROP DATABASE cinema_db_test WITH (FORCE)"))


app.dependency_overrides[session_transaction] = test_core.test_connection


@pytest.fixture(scope="session")
async def aclient():
    async with ASGITransport(app=app) as tr:
        aclient = AsyncClient(
            transport=tr,
            base_url="http://test",
        )
        yield aclient
