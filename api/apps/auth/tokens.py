from datetime import UTC, datetime, timedelta

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.config import settings
from api.db.schema import User as db_User
from api.loggers import api_logger


class JWTException(Exception):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


def create_access_token(
    data: dict,
    secret_key: str = settings.access_token.secret_key,
    algorithm: str = settings.access_token.algorithm,
    token_expire_minutes: int = settings.access_token.expire_minutes,
) -> str:
    to_encode = data.copy()
    default_expiry = datetime.now(tz=UTC) + timedelta(minutes=token_expire_minutes)
    to_encode.setdefault("exp", datetime.timestamp(default_expiry))
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


async def decode_access_token(
    session: AsyncSession,
    token: str,
    secret_key: str = settings.access_token.secret_key,
    algorithm: str = settings.access_token.algorithm,
) -> db_User:
    try:
        payload = jwt.decode(
            token, secret_key, algorithms=algorithm,
        )
    except ExpiredSignatureError:
        raise JWTException("Token has expired")
    except InvalidTokenError as e:
        api_logger.warning(f"Invalid token error: {e}")
        raise JWTException(f"Invalid token: {token}")
    username = payload.get("sub")

    async with session as s:
        user = (
            (await s.execute(select(db_User).where(db_User.username == username)))
            .scalars()
            .first()
        )

    if not user:
        api_logger.warning(f"User not found: {username}")
        raise JWTException(f"Invalid token: {token}")
    return user
