from settings import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine(
    f'postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}',
    encoding='utf-8',
    echo=False,
    pool_size=100,
    pool_recycle=10
)
