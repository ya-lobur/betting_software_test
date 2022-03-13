from db import Base
from settings import settings
from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from tornado_sqlalchemy import SQLAlchemy

db = SQLAlchemy(url=f'{settings.DB_HOST}:{settings.DB_PORT}')


class RequestModel(Base):
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True)
    rq_body_hash = Column(String, nullable=True)
    rq_body = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())
