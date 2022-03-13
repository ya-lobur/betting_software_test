import tornado.web
from db import engine
from handlers.api import ApiAddHandler, ApiDeleteHandler, ApiGetHandler
from settings import settings


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/api/add', ApiAddHandler),
            (r'/api/get', ApiGetHandler),
            (r'/api/remove/([\x00-\x7f]+)', ApiDeleteHandler),
        ]

        tornado.web.Application.__init__(self, handlers, debug=True)
        self.db_engine = engine


if __name__ == '__main__':
    Application().listen(settings.APP_PORT)
    tornado.ioloop.IOLoop.instance().start()
