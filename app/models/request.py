from db import Base
from settings import settings
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from tornado_sqlalchemy import SQLAlchemy

db = SQLAlchemy(url=f'{settings.DB_HOST}:{settings.DB_PORT}')


class RequestModel(Base):
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True)
    rq_body_hash = Column(String, nullable=True)
    rq_body = Column(JSONB, nullable=True)
