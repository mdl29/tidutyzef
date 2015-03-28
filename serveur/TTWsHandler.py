#-*- coding:utf-8 -*-
from tornado import websocket
import json
from utils import *

usernameNotSet =  (0,"you should have an username and a team before any operation")
teamError = (1,"this team doesn't exist")
usernameAlreadyUse = (2,"username already in use in your team")
JSONError = (3,"the JSON can't be load")
unknowObject = (4,"the object is not set or isn't recognized")
usernameAlreadySet = ( 5,"you can't change your username")
userChgParams = (6, "you can't change params if you're not admin")
unknowParameter = (7, "the parameter you're asking for doesn't exist")

class TTWsHandler(websocket.WebSocketHandler):
    """
    manage client connections
    """
    def check_origin(self, origin):
        return True

    def __init__(self,*args):
        self.debug = True
        super().__init__(*args)

    def sendError(self,error): # errors codes are defined in the global scope
        self.send({"object":"error","errorCode":error[0],"desc":error[1]})

    def send(self,msg):
        try:
            self.write_message(msg)
        except websocket.WebSocketClosedError:
            self.close()
        #d(self.debug,"send :",msg,"to : ",self.request.host,"on",self.request.path)

    def open(self):
        raise NotImplementedError

    def on_message(self,msg):
        """
        unparse the JSON
        """
        d(self.debug,"receive :",msg,"from :",self.request.host,"on",self.request.path)

        try:
            data = json.loads(msg)
            self.onMessage(data)
        except ValueError:
            self.sendError(JSONError)

    def on_close(self):
        raise NotImplementedError
