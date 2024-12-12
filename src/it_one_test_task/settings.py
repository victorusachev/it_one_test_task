import os
from typing import Literal

from pydantic import BaseModel, Field, FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class DatabaseSettings(BaseModel):
    host: str = Field(..., description='Database host address.')
    port: int = Field(..., description='Database port number.')
    name: str = Field(..., description='Database name.')
    username: str = Field(..., description='Database username.')
    password: str = Field(..., description='Database user password.')
    application: str = Field(..., description='Database client application name.')
    log_sql: bool = Field(False, description='Database query logging flag.')
    driver: Literal['postgresql+asyncpg'] = Field('postgresql+asyncpg', description='Driver name.')

    def get_url(self) -> 'URL':
        return URL.create(
            drivername='postgresql+asyncpg',
            username=self.username,
            password=self.password,
            database=self.name,
            host=self.host,
            port=self.port,
            query={'application_name': self.application},
        )


class Settings(BaseSettings):
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    logfile_path: FilePath = Field(..., description='Path to log file.')

    model_config = SettingsConfigDict(
        env_file=os.getenv('ENV', '.env'),
        env_nested_delimiter='__',
    )
