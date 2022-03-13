# betting_software_test

## Перед запуском

1. Установить зависимости из requirements.txt:

```shell
pip install -r requirements.txt
```

2. В корневой директории создать файл `.env.db` по подобию примера в .env.db.example
3. В директории `app/` создать файл `.env` по подобию примера в .env.example

## Для разработки

Установить пре-коммит хуки

```shell
pre-commit install
```

## Запуск

```shell
docker-compose up --build -d
```

Запросы можно кидать на `http://127.0.0.1:8888` + соответствующий роут