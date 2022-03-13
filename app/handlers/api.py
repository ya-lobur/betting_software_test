import json

import tornado.web
from models.request import RequestModel
from modules.request.use_cases import encode_rq_body
from sqlalchemy import func, insert, select


class HandlerWithEngineMixin(tornado.web.RequestHandler):
    @property
    def db_engine(self):
        return self.application.db_engine


class ApiAddHandler(HandlerWithEngineMixin):
    """
    Этот хэндлер занимается обработкой входящего тела запроса.
    POST:
        Сохраняет тело и хэш тела в базу.
        Возвращает json с ключом {'key': 'eyJrZXkiOiAiYWFhZHMgYXNkZCJ9'}
    """

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def post(self):
        rq_body = json.loads(self.request.body)
        rq_body_hash = encode_rq_body(rq_body)

        with self.db_engine.connect() as conn:
            conn.execute(
                insert(RequestModel).values(
                    rq_body_hash=rq_body_hash,
                    rq_body=rq_body
                )
            )

        self.write(
            json.dumps({
                'key': rq_body_hash
            })
        )


class ApiGetHandler(HandlerWithEngineMixin):
    """
       Возвращается тело искомого запроса, запроса с дополнительным полем “duplicates”.
    """

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get(self):
        key = self.get_arguments('key')
        if not key:
            self.set_status(400)
            self.write(
                json.dumps({
                    'message': 'Ключ key не указан в параметрах запроса'
                })
            )

        with self.db_engine.connect() as conn:
            body = conn.execute(
                select([RequestModel.rq_body]).where(
                    RequestModel.rq_body_hash.in_(key)
                )
            ).fetchone()

            body = body['rq_body'] if body else {}

            duplicates = conn.execute(
                select([func.count()]).where(
                    RequestModel.rq_body_hash.in_(key)
                )
            ).fetchone()

        response = {
            **body,
            'duplicates': duplicates[0]
        }

        self.write(
            json.dumps(response)
        )
