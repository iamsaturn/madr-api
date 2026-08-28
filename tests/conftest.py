import pytest_asyncio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer
from madr_api.app import app
from madr_api.database import get_session, table_registry
from madr_api.schemas import UserCreate
from tests.schemas import TestUser

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


@pytest.fixture
def user_data():
    return UserCreate(
                username= 'Maria',
                email= 'maria@gmail.com',
                password='mariasecret'
            )

@pytest.fixture
def other_user_data():
    return UserCreate(
            username= 'Lua',
            email= 'lua@gmail.com',
            password='luasecret'
        )

@pytest.fixture
def test_user(client,user_data):
    response = client.post(
        '/users', json=user_data.model_dump(mode='json')
    )
    data = response.json()
    data['clear_password'] = user_data.password
    return TestUser.model_validate(data)

@pytest.fixture
def token(client,test_user):
    response = client.post('/auth/token',
                data={
                    'username': test_user.email,
                    'password': test_user.clear_password
                })
    token = response.json()['access_token']
    return token

@pytest.fixture
def headers(token):
    return {'Authorization': f'Bearer {token}'}
    