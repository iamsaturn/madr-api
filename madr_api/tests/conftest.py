import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer
from madr_api.app import app
from madr_api.database import get_session, table_registry

container = PostgresContainer(
    image='postgres:17', driver='psycopg'
)

@pytest_asyncio.fixture(scope="session")
async def engine():
    with container as postgres:
        engine = create_async_engine(postgres.get_connection_url())
        yield engine
        await engine.dispose()

@pytest_asyncio.fixture
async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)

@pytest_asyncio.fixture
async def session(engine, create_tables):
    Session = async_sessionmaker(engine)
    async with Session() as session:
        yield session


@pytest_asyncio.fixture
async def client(session):
    async def override_get_session():
        yield session
    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()


