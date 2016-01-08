#!/usr/bin/python3
"""
Start the game server
"""

from tornado import web, ioloop
import tornado.options

from playerws import PlayerWs
from adminws import AdminWs
from game import Game

SOCKET_PORT = 8080

if __name__ == "__main__":
    tornado.options.parse_command_line()


    web.Application([(r'/', PlayerWs),
                     (r'/admin', AdminWs)]
                   ).listen(SOCKET_PORT)
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        Game().stop()
