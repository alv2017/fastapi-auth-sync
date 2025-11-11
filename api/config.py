import logging
import os
from enum import Enum
from pathlib import Path

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

ROOT_DIRECTORY = Path(__file__).parent.parent
ENV = ROOT_DIRECTORY / ".env"
ENV_TEMPLATE = ROOT_DIRECTORY / ".env.template"
API_LOG_FILE_LOCATION = ROOT_DIRECTORY / "logs" / "api.log"


class RunMode(str, Enum):
    DEV: str = "DEV"
    PROD: str = "PROD"
    TEST: str = "TEST"


class LoggingMode(Enum):
    CRITICAL: int = logging.CRITICAL
    ERROR: int = logging.ERROR
    WARNING: int = logging.WARNING
    INFO: int = logging.INFO
    DEBUG: int = logging.DEBUG


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    logging: int = LoggingMode.ERROR
    reload: bool = True
    mode: str = RunMode.PROD.value


class AccessTokenConfig(BaseModel):
    secret_key: str = "ChangeMe-Secret-Key-2025"
    algorithm: str = "HS256"
    expire_minutes: int = 30


class DBConfig(BaseModel):
    vendor: str = "sqlite"
    iface: str = "aiosqlite"
    host: str = ""
    port: str = ""
    user: str = ""
    name: str = os.path.join(ROOT_DIRECTORY, "sqlite", "db.sqlite")
    password: str = ""
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    prepared_statement_cache_size: int = 128
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
            query={
                "prepared_statement_cache_size": str(self.prepared_statement_cache_size)
            },
        )


class Settings(BaseSettings):
    api_prefix: str = "/api"
    run: RunConfig = RunConfig()
    db: DBConfig = DBConfig()
    access_token: AccessTokenConfig = AccessTokenConfig()

    model_config = SettingsConfigDict(
        env_file=(ENV_TEMPLATE, ENV), case_sensitive=False, env_nested_delimiter="__"
    )


settings = Settings()

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
