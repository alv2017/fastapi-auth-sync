import pytest

from api.main import app


@pytest.fixture(scope="session")
def test_db_engine():
    from api.db.connectors import _get_async_engine

    engine = _get_async_engine()
    yield engine


@pytest.fixture
async def async_test_session(test_db_engine):
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
    from api.db.schema import Base

    AsyncSessionLocal = async_sessionmaker(
        bind=test_db_engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with test_db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        yield session

    async with test_db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_test_client(async_test_session):
    from httpx import AsyncClient, ASGITransport
    from api.db.connectors import get_async_session

    async def override_get_async_session():
        yield async_test_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        yield client

    app.dependency_overrides.clear()
