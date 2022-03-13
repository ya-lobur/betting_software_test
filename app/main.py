import tornado.web
from db import engine
from handlers.api import ApiAddHandler, ApiGetHandler
from settings import settings


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/api/add', ApiAddHandler),
            (r'/api/get', ApiGetHandler),
        ]

        tornado.web.Application.__init__(self, handlers, debug=True)
        self.db_engine = engine


if __name__ == '__main__':
    Application().listen(settings.APP_PORT)
    tornado.ioloop.IOLoop.instance().start()
