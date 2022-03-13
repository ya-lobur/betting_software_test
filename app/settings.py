from typing import Union

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_PORT = 8888
    DB_NAME = 'bs_database'
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = '127.0.0.1'
    DB_PORT: Union[int, str] = 5432


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
