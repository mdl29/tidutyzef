#!/usr/bin/python3
#-*- coding:utf-8 -*-

from tornado import websocket, web, ioloop
import tornado.options
tornado.options.parse_command_line()
from Player import *
from Admin import *
from Game import *
import sys

SOCKET_PORT = 8080

if __name__=="__main__":
    game=Game()
    app=web.Application([
        (r'/', Player),
        (r'/admin',Admin)])
    app.listen(SOCKET_PORT)
    ioloop.IOLoop.instance().start()
