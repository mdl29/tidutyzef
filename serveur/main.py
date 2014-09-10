#!/usr/bin/python3
#-*- coding:utf-8 -*-

from TTWebSocketServer import *
from TTClientConnection import *
import sys

if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1] == "debug":
        debug = True
    else:
        debug = False
    print("debug :",debug)
    ws=TTWebSocketServer(debug)
    ws.join()
