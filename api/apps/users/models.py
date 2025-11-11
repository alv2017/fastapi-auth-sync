from fastapi.param_functions import Form
from pydantic import BaseModel
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


class ResponseUserModel(UserBaseModel):
    id: int
