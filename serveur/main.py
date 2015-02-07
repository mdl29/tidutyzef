#!/usr/bin/python3
#-*- coding:utf-8 -*-

from tornado import websocket, web, ioloop
from Player import *
from Admin import *
from Game import *
import sys

SOCKET_PORT = 9876

if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1] == "debug":
        debug = True
    else:
        debug = False
    print("debug :",debug)

    game=Game()
    app=web.Application([
        (r'/', Player),
        (r'/admin',Admin)])
    app.listen(SOCKET_PORT)
    ioloop.IOLoop.instance().start()
