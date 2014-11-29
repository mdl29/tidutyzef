#-*- coding:utf-8 -*-

from pyWebSocket import WebSocketServer, WebSocketClient
from TTWebSocketServer import *
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

class errorParentIsnotTTWebSocketServer (Exception):
        def __init__(self):
            BaseException.__init__(self)

class TTClientConnection(WebSocketClient):
    """
    manage client connections
    """

    def __init__(self, parent, sock, addr):
        """
        init the connectiion
        """
        self.debug = parent.debug
        
        # Used for debuging purpose
        self.username = "NOT_LOGGED"
        self.team = "NOT_LOGGED"
        
        WebSocketClient.__init__(self, parent, sock, addr)

    def sendError(self,error): # errors codes are defined in the global scope
        self.send({"object":"error","errorCode":error[0],"desc":error[1]})

    def send(self,msg):
        WebSocketClient.send(self,json.dumps(msg))
        d(self.debug,"send :",msg,"to :",self.username,"of the team",self.team)

    def onReceive(self,msg):
        """
        unparse the JSON
        """
        d(self.debug,"receive :",msg,"from :", self.username,"of the team",self.team)
        try:
            data = json.loads(msg)
            return data
        except ValueError:
            self.sendError(JSONError)

    def onConnectionClose(self):
        """
        connection closing handler
        """
        self.send({"object" :"logout","user1 ":self.username})
        self.parent.send2All({"object" :"connection","user":self.username,"status":"logout"})
        for client in self.parent.client:
            if client==self: 
                self.parent.delClient(self)
