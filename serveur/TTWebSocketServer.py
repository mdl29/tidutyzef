#-*- coding:utf-8 -*-

from pyWebSocket import WebSocketServer, WebSocketClient
from TTClientConnection import *
import threading, json, re, utils
from zone import *
from Params import *
from Player import *

class TTWebSocketServer(WebSocketServer):
    def __init__(self):
        WebSocketServer.__init__(self,clientClass = Player)
        self.teams = {'tizef':[],'tidu':[],'admin':[]}
        self.params = Params()
        self.threadCheckBattle = threading.Thread(target=self.checkBattle)
        self.threadCheckBattle.daemon = True
        self.threadCheckBattle.start()

    """
    this is util for checking for battles entering in zone
    """
    def checkBattle(self):
        self.keepAlive.set()
        while self.keepAlive.isSet(): # keepAlive is already set in pyWebSocket
            for index,value in enumerate(self.teams["tidu"]):
                if value.statuts != 1:
                    continue
                a = len(self.client) - 1 - index
                for index2,value2 in enumerate(self.teams["tizef"]):
                    #print("test :", value.username, "of the team tidu","and",value2.username, "of the team tizef")
                    if value2.status != 1:
                        continue
                    if utils.distance(value.pos,value2.pos) <= self.params.getParams("radius"):
                        print("beginning of a battle between :", value.username, "of the team tidu","and",value2.username, "of the team tizef")
                        tmpSup = BattleSupervisor(value2,value)
                        value.startBattle(value2,tmpSup)
                        value2.startBattle(value,tmpSup)

            for index,client in enumerate(self.client):
                if client.statuts is not "playing" or client.statuts is not "kill":
                    continue
                for index,zone in enumerate(self.params.getParams(zones)):
                    if utils.distance(zone.team,client.team) <= self.params.getParams("radius"):
                        zone.addPlayerInRadius(client)
            sleep(0.5)
                    
    def delClient(self,client):
        for index, aClient in enumerate(self.teams[client.team]) :
            if aClient == client:
                self.teams[client.team].pop(index)
        for index, aClient in enumerate(self.client) :
            if aClient == client:
                self.client.pop(index)    
        print("del the client : " + client.username)

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

    def setParams(self,data):
        if username == "admin":
            self.params.setParams(data)
