#-*- coding:utf-8 -*-

from pyWebSocket import WebSocketServer, WebSocketClient
from TTClientConnection import *
import threading, json

class TTWebSocketServer(WebSocketServer):
    def __init__(self):
        WebSocketServer.__init__(self,clientClass = TTClientConnection)
        self.teams = {'tizef':[],'tidu':[]}
        self.zones = {'tizef':[],'tidu':[],'any':[]}

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
    """
    check if any user in your team have your pseudo and if your team exist
    return 0 if there isn't any error, 1 if team doesn't exist and 2 if the username already exist in your team
    """
    def addUser2Team(self,username,team,client):
        if not team in self.teams:
            return 1
        for aClient in self.client:
            if aClient.username==username and aClient.team==team:
                return 2
        self.teams[team].append(client)

