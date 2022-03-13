from db import Base
from sqlalchemy import BigInteger, Column, Integer, String, delete, func, select
from sqlalchemy.dialects.postgresql import JSONB


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

    @staticmethod
    def get_statistic(conn):
        """
        В теории может быть больше 100% это будет значить что дублей больше, чем уникальных запросов
        """

        unique_rq_count = conn.execute(
            select([func.count()]).select_from(RequestModel)
        ).scalar()

        duplicates_sum = conn.execute(
            select([func.sum(RequestModel.duplicates)]).select_from(RequestModel)
        ).scalar()

        if duplicates_sum or unique_rq_count > 0:
            return (duplicates_sum / (unique_rq_count + duplicates_sum)) * 100
