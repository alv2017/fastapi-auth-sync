from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.apps.auth.passwords import hash_password
from api.apps.users.models import CreateUserModel
from api.db.schema import User as db_User
from api.loggers import api_logger


async def _create_user(db_session: AsyncSession, new_user: CreateUserModel) -> db_User:
    hashed_password: str = hash_password(new_user.password)
    db_user = db_User(
        username=new_user.username,
        email=new_user.email,
        hashed_password=hashed_password,
    )

    async with db_session as session:
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

    return db_user


async def create_user(db_session: AsyncSession, new_user: CreateUserModel) -> db_User:
    try:
        user = await _create_user(db_session, new_user)
    except IntegrityError:
        msg = "DB IntegrityError: User with given username or email already exists."
        raise ValueError(msg)
    except Exception as e:
        api_logger.error(f"Unexpected Error: user creation in db failed: {e}")
        raise RuntimeError(f"Failed to create user: {e}")
    return user


async def get_user_by_username(username: str, db_session: AsyncSession) -> db_User:
    async with db_session as session:
        user = (
            (await session.execute(select(db_User).where(db_User.username == username)))
            .scalars()
            .first()
        )
    if not user:
        raise ValueError(f"User not found: {username}")
    return user
