#!/usr/bin/env python
#-*- coding:utf-8 -*-

from TTWebSocketServer import *
from TTClientConnection import *

if __name__=="__main__":
    ws=TTWebSocketServer()
    ws.join()
