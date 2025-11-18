from email_validator import EmailNotValidError, validate_email
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.apps.auth.passwords import verify_password
from api.db.schema import User as db_User


class AuthenticationError(Exception):
    pass


async def authenticate_user(
    session: AsyncSession, username_or_email: str, password: str
) -> db_User:
    try:
        validate_email(username_or_email)
        query_filter = db_User.email
    except EmailNotValidError:
        query_filter = db_User.username

    async with session:
        user = (
            (
                await session.execute(
                    select(db_User).where(query_filter == username_or_email)
                )
            )
            .scalars()
            .first()
        )

    if not user:
        raise AuthenticationError(f"Invalid credentials for user: {username_or_email}")

    if not verify_password(password, user.hashed_password):
        raise AuthenticationError(f"Invalid credentials for user: {username_or_email}")

    return user


# Function to reverse an integer: example: 123 -> 321
