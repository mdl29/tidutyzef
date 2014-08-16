#!/usr/bin/env python
#-*- coding:utf-8 -*-

from pyWebSocket import WebSocketServer, WebSocketClient
import threading, json

class errorParentIsnotTTWebSocketServer (Exception):
        def __init__(self):
            BaseException.__init__(self)

class TTWebSocketServer(WebSocketServer):
    def __init__(self):
        WebSocketServer.__init__(self,clientClass = TTClientConnection)
        self.teams = {'tizef':[],'tidu':[]}
    def delClient(self,client):
        for index, aClient in enumerate(self.client) :
            if aClient == client:
                self.client.pop(index)    
        print("del the client : "+client.username)  
    def send2team(self,data,team):
        for index, client in enumerate(self.teams[team]) :
            try:
                client.send(msg)
            except socket.error :
                self.client.pop(index)    

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
        
    def onReceive(self,msg):
        """
        receive handler
        """
        try:
            data = json.loads(msg)
        except ValueError as e:
            self.send(json.dumps({"error":3,"desc":str(e)}))
            return
        if not self.username and not "username" in data:
            self.send(json.dumps({"object" : "error", "errorCode":1,"desc":"you must have an username"}))
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
            self.send(json.dumps({"object" : "error", "errorCode":3,"desc":"object " + data["object"] + " is not set or it isn't recognized"}))
            
    def login (self,data):
        if "username" in data and "team" in data:          #username change
            for client in self.parent.client:
                if client.username==data["username"] and client.team==data["team"]:
                    self.send(json.dumps({"object" : "error", "errorCode":0,"desc":"username already in use in your team"}))
                    break
            else:
                if not self.username:
                    self.username = data["username"]
                    self.team = data["team"]
                    self.parent.send2All(json.dumps({"object" : "connection", "user":self.username,"status":"login"}))
                    self.send(json.dumps({"object" :"login","user":self.username}))
                else:
                    self.send(json.dumps({"object" : "error", "errorCode":4,"desc":"You can't change your username"}))
    
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
