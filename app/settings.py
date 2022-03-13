from typing import Union

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_NAME = 'bs_database'
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = '127.0.0.1'
    DB_PORT: Union[int, str] = 5432


settings = Settings(_env_file='dev.env', _env_file_encoding='utf-8')