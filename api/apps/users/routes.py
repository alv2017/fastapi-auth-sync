from fastapi import APIRouter, Depends, HTTPException, status

from api.apps.auth.tokens import JWTException, decode_access_token
from api.apps.users.db_ops import create_user
from api.apps.users.models import CreateUserModel, ResponseUserModel
from api.config import oauth2_scheme
from api.db.connectors import get_async_session
from api.db.schema import User as db_User
from api.loggers import api_logger

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_user(
    new_user: CreateUserModel, session=Depends(get_async_session)
) -> ResponseUserModel:
    try:
        db_user = await create_user(db_session=session, new_user=new_user)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with provided username or email already exists",
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"User creation failed: {e}",
        )
    except Exception as e:
        api_logger.error(f"Unexpected error during user registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {e}",
        )
    else:
        user_data = db_user.__dict__
        return ResponseUserModel(**user_data)


@router.get("/me/", status_code=status.HTTP_200_OK)
async def get_user_me(
    token: str = Depends(oauth2_scheme), session=Depends(get_async_session)
) -> ResponseUserModel:
    try:
        user: db_User = await decode_access_token(token=token, session=session)
    except JWTException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Access Forbidden: {e}"
        )

    return ResponseUserModel(**user.__dict__)
