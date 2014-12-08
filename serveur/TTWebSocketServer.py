#-*- coding:utf-8 -*-

from pyWebSocket import WebSocketServer, WebSocketClient
from TTClientConnection import *
import threading, json, re, utils
from zone import *
from Params import *
from Player import *
from battle import *
import time

class TTWebSocketServer(WebSocketServer):
    def __init__(self,debug = False):
        if debug:
            self.debug = True
        else:
            self.debug = False
        WebSocketServer.__init__(self,clientClass = Player)
        self.teams = {'tizef':[],'tidu':[],'admin':[]}
        self.params = Params(self)
        self.gameStarted = False
        self.canStartBattle = threading.Event()
        self.canStartBattle.set()

    def endGame(self,cause):
        out = {"object":"endGame","cause":cause}
        self.send2All(out)
        self.gameStarted = False

    def startGame(self):
        self.threadUpdate = threading.Thread(target=self.update)
        self.threadUpdate.daemon = True
        self.gameStarted = True
        for client in self.client:
            if client.status == "other":
                continue
            else:
                client.status = "playing"
        self.threadUpdate.start()

    def update(self):
        t1 = time.time()
        while self.gameStarted or self.keepAlive.isSet():
            if not self.teams["tidu"] or  not self.teams["tizef"]:
                self.endGame("noEnoughPlayer")
                break
            """
            time test
            """
            t = time.time() - t1
            timeout = self.params.getParams("time")
            if t >= timeout:
                self.endGame("timeout")
                break
            """
            test victory
            """
            tiduZone = 0
            tizefZone = 0
            for zone,_ in enumerate(self.params.getParams("zones")):
                if not isinstance(zone,Zone):
                    break
                if zone.team == "tidu":
                    tiduZone += 1
                elif zone.team == "tizef":
                    tizefZone += 1
            tiduAlive = 0
            tizefAlive = 0
            for tidu in self.teams["tidu"]:
                if tidu.status is not "kill":
                    tiduAlive += 1
            for tizef in self.teams["tizef"]:
                if tizef.status is not "kill":
                    tizefAlive += 1
            if tiduAlive == 0 and tiduZone == 0:
                self.endGame("tizefWin")
                break
            if tizefAlive == 0 and tizefZone == 0:
                self.endGame("tiduWin")
                break
            """
            zones test
            """

            for index,client in enumerate(self.client):
                if client.status is not "playing" or client.status is not "kill":
                    continue
                for index,zone in enumerate(self.params.getParams(zones)):
                    if utils.distance(zone.team,client.team) <= self.params.getParams("radius"):
                        zone.addPlayerInRadius(client)

    def checkBattle(self,player):
        self.canStartBattle.wait()
        self.canStartBattle.clear()

        if player.status != "playing":
            return
        if player.team == "tizef":
            team = "tizef"
        elif player.team == "tidu":
            team = "tidu"
        for index2,value2 in enumerate(self.teams[team]):
            if value2.status != "playing":
                continue
            d(self.debug,"test battle :", player.username, "of the team tidu","and",value2.username, "of the team tizef")
            if utils.distance(player.pos,value2.pos) <= self.params.getParams("radius"):
                d(self.debug,"beginning of a battle between :", player.username, "of the team tidu","and",value2.username, "of the team tizef")
                tmpBattle = Battle(value2,player)
                player.startBattle(value2,tmpBattle)
                value2.startBattle(player,tmpBattle)
        self.canStartBattle.clear()

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
        self.params.setParams(data)

    def getParams(self,params):
        return self.params.getParams(params)
