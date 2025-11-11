from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.apps.auth.authenticate import AuthenticationError, authenticate_user
from api.apps.auth.tokens import Token, create_access_token
from api.db.connectors import get_async_session
from api.db.schema import User as db_User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token/")
async def get_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> Token:
    try:
        user: db_User = await authenticate_user(
            session=session,
            username_or_email=form_data.username,
            password=form_data.password,
        )
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    jwt_string = create_access_token(data={"sub": user.username})
    return Token(access_token=jwt_string)
