from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import registry

from madr_api.settings import settings

engine = create_async_engine(settings.DATABASE_URL)
Session = async_sessionmaker(
    engine,
    expire_on_commit=False)


async def get_session():
    async with Session() as session:
        yield session


table_registry = registry()
