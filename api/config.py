import logging
from enum import Enum
from pathlib import Path

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

ROOT_DIRECTORY = Path(__file__).parent.parent
ENV = ROOT_DIRECTORY / ".env"
API_LOG_FILE_LOCATION = ROOT_DIRECTORY / "logs" / "api.log"


class RunMode(str, Enum):
    DEV = "DEV"
    PROD = "PROD"
    TEST = "TEST"


class LoggingMode(Enum):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    logging: int = LoggingMode.ERROR.value
    reload: bool = True
    mode: str = RunMode.PROD.value


class AccessTokenConfig(BaseModel):
    secret_key: str
    algorithm: str = "HS256"
    expire_minutes: int = 30


class DBConfig(BaseModel):
    vendor: str
    iface: str
    host: str
    port: str
    user: str
    name: str
    password: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=f"{self.vendor}+{self.iface}",
            username=self.user or None,
            password=self.password or None,
            host=self.host or None,
            port=int(self.port) if self.port else None,
            database=self.name or None,
        )


class Settings(BaseSettings):
    api_prefix: str = "/api"
    run: RunConfig
    db: DBConfig
    access_token: AccessTokenConfig

    model_config = SettingsConfigDict(
        env_file=ENV, case_sensitive=False, env_nested_delimiter="__"
    )


settings = Settings()


oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
