from datetime import UTC, datetime, timedelta

import pytest

from api.apps.auth.tokens import create_access_token
from api.main import app


@pytest.fixture
def user_data():
    return {
        "username": "test-user",
        "email": "test-user@example.com",
        "password": "Strong-Unbreakable-Password-07",
    }


@pytest.fixture()
def test_db_engine():
    from api.db.connectors import _get_async_engine

    engine = _get_async_engine()
    yield engine


@pytest.fixture
async def async_test_db_session(test_db_engine):
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
async def async_test_db_session_with_user(async_test_db_session, user_data):
    from api.apps.auth.passwords import hash_password
    from api.db.schema import User as db_User

    db_user = db_User(
        username=user_data["username"],
        email=user_data["email"],
        hashed_password=hash_password(user_data["password"]),
    )
    async with async_test_db_session as session:
        session.add(db_user)
        await session.commit()
        yield async_test_db_session


@pytest.fixture
async def async_test_client():
    from httpx import ASGITransport, AsyncClient

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client


@pytest.fixture
async def async_test_client_with_db_access(async_test_db_session):
    from httpx import ASGITransport, AsyncClient

    from api.db.connectors import get_async_session

    async def override_get_async_session():
        yield async_test_db_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def async_test_client_with_db_access_and_db_user(async_test_db_session_with_user):
    from httpx import ASGITransport, AsyncClient

    from api.db.connectors import get_async_session

    async def override_get_async_session():
        yield async_test_db_session_with_user

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def async_authorized_test_client(
    async_test_client_with_db_access_and_db_user, user_data
):
    from api.apps.auth.tokens import create_access_token

    token = create_access_token(data={"sub": user_data["username"]})
    async_test_client_with_db_access_and_db_user.headers.update(
        {"Authorization": f"Bearer {token}"}
    )
    yield async_test_client_with_db_access_and_db_user


@pytest.fixture
async def async_test_client_with_expired_token(
    async_test_client_with_db_access_and_db_user, user_data
):
    expire_time = datetime.now(tz=UTC) + timedelta(minutes=-1)
    token = create_access_token(
        data={"sub": user_data["username"], "exp": datetime.timestamp(expire_time)}
    )
    async_test_client_with_db_access_and_db_user.headers.update(
        {"Authorization": f"Bearer {token}"}
    )
    yield async_test_client_with_db_access_and_db_user


@pytest.fixture
async def async_test_client_with_faked_token(
    async_test_client_with_db_access_and_db_user,
):
    fake_user = {
        "username": "fake-user",
    }
    token = create_access_token(data={"sub": fake_user["username"]})
    async_test_client_with_db_access_and_db_user.headers.update(
        {"Authorization": f"Bearer {token}"}
    )
    yield async_test_client_with_db_access_and_db_user


@pytest.fixture
async def async_test_client_with_invalid_token(
    async_test_client_with_db_access_and_db_user,
):
    invalid_token = "this.is.a.random.token.20251118"
    async_test_client_with_db_access_and_db_user.headers.update(
        {"Authorization": f"Bearer {invalid_token}"}
    )
    yield async_test_client_with_db_access_and_db_user
