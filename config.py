from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr

    class Config:
        env_file='./.env'
        env_file_encoding='utf-8'
        env_nested_delimiter='__'

CONFIG = Settings()
