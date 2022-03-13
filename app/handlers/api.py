import json

import tornado.web
from models.request import RequestModel
from modules.request.use_cases import encode_rq_body
from sqlalchemy import insert, select, update


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
            duplicates = RequestModel.get_duplicates(conn, rq_body_hash)

            if duplicates is not None:
                conn.execute(
                    update(RequestModel).where(
                        RequestModel.rq_body_hash == rq_body_hash
                    ).values(
                        duplicates=duplicates + 1
                    )
                )
            else:
                conn.execute(
                    insert(RequestModel).values(
                        rq_body_hash=rq_body_hash,
                        rq_body=rq_body,
                        duplicates=0
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
                select([RequestModel.rq_body, RequestModel.duplicates]).where(
                    RequestModel.rq_body_hash.in_(key)
                )
            ).fetchone()

        response = {'duplicates': 0}

        if body:
            response = {
                'request_body': body['rq_body'],
                'duplicates': body['duplicates']
            }

        self.write(
            json.dumps(response)
        )


class ApiDeleteHandler(HandlerWithEngineMixin):
    """
       Удаляем запрос по ключу.
    """

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def delete(self, body_hash):
        with self.db_engine.connect() as conn:
            RequestModel.delete_request_by_body_hash(conn, body_hash)

        self.write(
            json.dumps({
                'message': 'Успешно удалено'
            })
        )


class ApiUpdateHandler(HandlerWithEngineMixin):
    """
    PUT:
        Обновляет тело и хэш тела.
        Возвращает json с ключом {'key': 'eyJrZXkiOiAiYWFhZHMgYXNkZCJ9'}
    """

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def put(self, old_body_hash):
        rq_body = json.loads(self.request.body)
        new_body_hash = encode_rq_body(rq_body)

        with self.db_engine.connect() as conn:
            is_exist = RequestModel.get_duplicates(conn, old_body_hash)

            if is_exist is not None:
                duplicates = RequestModel.get_duplicates(conn, new_body_hash)
                if duplicates:
                    conn.execute(
                        update(RequestModel).where(
                            RequestModel.rq_body_hash == new_body_hash
                        ).values(
                            duplicates=duplicates + 1
                        )
                    )
                else:
                    conn.execute(
                        insert(RequestModel).values(
                            rq_body_hash=new_body_hash,
                            rq_body=rq_body,
                            duplicates=0
                        )
                    )
                RequestModel.delete_request_by_body_hash(conn, old_body_hash)
            else:
                self.set_status(400)
                self.write(
                    json.dumps({
                        'message': f'По ключу {old_body_hash} ничего не было найдено'
                    })
                )
                return

        self.write(
            json.dumps({
                'key': new_body_hash
            })
        )


class ApiStatisticHandler(HandlerWithEngineMixin):
    """
    Получаем % дубликатов от количества общих запросов.
    В теории может быть больше 100% это будет значить что дублей больше, чем уникальных запросов
    """

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get(self):
        with self.db_engine.connect() as conn:
            result = RequestModel.get_statistic(conn)

        self.write(
            json.dumps({
                'result': f'{float(result)} %' if result is not None else result
            })
        )
