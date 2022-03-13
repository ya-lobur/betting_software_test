import base64
import json


def encode_rq_body(body: dict) -> str:
    """
    Создает хэш для JSON-а который нам приходит в /api/add


    :param body: тело запроса в виде словаря
    :return: строка закодированная в base64
    """

    encoded = json.dumps(body, sort_keys=True).encode()
    return base64.b64encode(encoded).decode('ascii')
