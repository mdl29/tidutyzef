#!/usr/bin/env python
#-*- coding:utf-8 -*-

import  json
from TTWebSocketServeur import *

usernameNotSet =  (0,"you should have an username and a team before any operation")
teamError = (1,"this team doesn't exist")
usernameAlreadyUse = (2,"username already in use in your team")
JSONError = (3,"the JSON can't be load")
unknowObject = (4,"the object is not set or isn't recognized")
usernameAlreadySet = ( 5,"you can't change your username")

class errorParentIsnotTTWebSocketServer (Exception):
        def __init__(self):
            BaseException.__init__(self)

class TTClientConnection(WebSocketClient):
    """
    manage client connections
    """

    def __init__(self, parent, sock, addr):
        """
        init the connection
        """
        if not isinstance(parent,TTWebSocketServer):
            raise errorParentIsnotTTWebSocketServer
        WebSocketClient.__init__(self, parent, sock, addr)
        self.pos = (0,0) # (latitude,longitude)
        self.username=""
        self.team=""
    def sendError(self,error): # errors codes are defined in the global scope
        self.send(json.dumps({"object":"error","errorCode":error[0],"desc":error[1]}))

    def onReceive(self,msg):
        """
        receive handler
        """
        try:
            data = json.loads(msg)
        except ValueError:
            self.sendError(JSONError)
            return
        if not self.username and not "username" in data:
            self.sendError(usernameNotSet)
            return
        print(msg)
        """
        the case keyword doesn't exist in python, so, we use a dictionary of function to call the appropriated function
        we use lambda to call 2 function or to modify the number of args to pass to the function
        """
        try:
            {"login" : lambda : self.login(data),
                    "updatePos" : lambda : self.updatePos(data),
                    "msg" : lambda : self.msg(data),
                    "logout" : lambda : self.onConnectionClose()
            }[data["object"]]()
        except KeyError:
            self.sendError(unknowObject)
            
    def login (self,data):
        if "username" in data and "team" in data:          #set username                
            if not self.username:
                error = self.parent.addUser2Team(data["username"],data["team"],self)
                if error:
                    if error == 1:
                        self.sendError(teamError)
                    if error == 2:
                        self.sendError(usernameAlreadyUse)
                else:
                    self.username = data["username"]
                    self.team = data["team"]
                    self.parent.send2All(json.dumps({"object" : "connection", "user":self.username,"status":"login"}))
                    self.send(json.dumps({"object" :"login","user":self.username}))
            else:
                self.sendError(usernameAlreadySet)
    
    def msg (self,data):
        if "msg" in data:  
            if "to" in data:
                for dest in data["to"]:
                    for client in self.parent.client:
                        if client.username==dest:
                            client.send(json.dumps({"object" : "msg", "from":self.username,"msg":data["msg"],"private":True}))
            else:
                self.parent.send2All(json.dumps({"object" : "msg", "from":self.username,"msg":data["msg"],"private":False}))
    
    def updatePos(self,data):
        self.pos = (data["lat"],data["lng"])
        self.parent.send2All(json.dumps({"object" : "updatePos", "from":self.username,"pos":self.pos,"team":self.team}))
    
    def onConnectionClose(self):
        """
        connection closing handler
        """
        self.send(json.dumps({"object" :"logout","user1 ":self.username}))
        self.parent.send2All(json.dumps({"object" :"connection","user":self.username,"status":"logout"}))
        for client in self.parent.client:
            if client.username==self.username: 
                self.parent.delClient(self)
                del client  #inutile car TTWebSocketServer pop de l'array le client et le supprime
        
if __name__=="__main__":
    ws=TTWebSocketServer()
    ws.join()
