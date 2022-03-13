from db import Base
from settings import settings
from sqlalchemy import BigInteger, Column, Integer, String, delete, select
from sqlalchemy.dialects.postgresql import JSONB
from tornado_sqlalchemy import SQLAlchemy

db = SQLAlchemy(url=f'{settings.DB_HOST}:{settings.DB_PORT}')


class RequestModel(Base):
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True)
    rq_body_hash = Column(String, nullable=False, unique=True)
    rq_body = Column(JSONB, nullable=False)
    duplicates = Column(BigInteger, nullable=False)

    @staticmethod
    def get_duplicates(conn, body_hash: str) -> int:
        result = conn.execute(
            select([RequestModel.duplicates]).where(
                RequestModel.rq_body_hash == body_hash
            )
        ).fetchone()

        return result[0] if result else None

    @staticmethod
    def delete_request_by_body_hash(conn, body_hash):
        conn.execute(
            delete(RequestModel).where(
                RequestModel.rq_body_hash == body_hash
            )
        )
