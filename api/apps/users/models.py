from fastapi.param_functions import Form
from pydantic import BaseModel, field_validator
from typing_extensions import Annotated, Doc


class UserBaseModel(BaseModel):
    username: str
    email: str


class CreateUserModel(UserBaseModel):
    password: Annotated[
        str,
        Form(json_schema_extra={"format": "password"}),
        Doc(
            """
                `password` string. The OAuth2 spec requires the exact field name
                `password`.
                """
        ),
    ]

    @field_validator("username")
    @classmethod
    def username_must_be_at_least_3_chars(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return v


class ResponseUserModel(UserBaseModel):
    id: int
