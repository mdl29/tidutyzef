import Params
import time
import threading
from utils import *
from Battle import *

class Game:
    """
    The main game Class, it's a singleton class
    """
    __shared_state = {}#for singleton
    __register = False

    def __init__(self):
        self.__dict__ = self.__shared_state#for singleton
        if not self.__register:
            self._init_default_register()

    def _init_default_register(self):
        self.__register = True
        self.zones = set()
        self.players = dict()
        self.lowerID = 0
        self.highterID = 0
        self.toCheck = set()
        self.admin = None
        self.params = Params.Params()
        self.gameStarted = False



    def endGame(self,cause):
        out = {"object":"endGame","cause":cause}
        self.send2All(out)
        self.gameStarted = False


    def send2All(self,msg):
        for _,player in self.players.items():
            player.send(msg)

    def send2Team(self,msg,team):
        tidu = True if team=="tidu" else False
        for id,player in (self.players):
            if (id > 0) == tidu: # send if it's the player aim to to good team
                player.send(msg)

    def addPlayer(self,player):
        if player.team is None:
            raise Exception("Player haven't any team !")
            return
        if player.team == "tidu":
            self.highterID += 1
            self.players[self.highterID] = player
            ID = self.highterID
        elif player.team == "tizef":
            self.lowerID -= 1
            self.players[self.lowerID] = player
            ID = self.lowerID
            print(self.lowerID)
        else:
            raise Exception("Team {} don't exist !".format(player.team))
        return ID

    def removePlayer(self,ID):
        if ID in self.players:
            del self.players[ID]
        if ID in self.toCheck:
            self.toCheck.remove(ID)

    def setAdmin(self,admin):
        if self.admin is not None:
            raise Exception("admin already set")
        else:
            self.admin = admin

    def unsetAdmin(self):
        del self.admin

    def getPlayerByID(self,id):
        if id in self.players:
            return self.players[id]
        else:
            raise Exception("Player's ID {} don't exist".format(id))

    def checkZones(self):
        for zone in self.zones:
            zone.update()

    def update(self):
        self.tStart = time.time()
        while self.gameStarted:
            if len(self.players) < 2:
                self.endGame("noEnoughPlayer")
                break

            if len(self.toCheck) is not 0:
                toCheck2 = set(self.toCheck)
                for player in toCheck2:
                    self.checkBattle(player)
                    self.toCheck.remove(player)
                self.checkVictory()
                self.checkZones()

    def setParams(self,data):
        self.params.setParams(data)

    def getParams(self,params):
        return self.params.getParams(params)

    def addPlayerToBattle(self,ID):
        self.toCheck.add(ID)

    def startGame(self):
        if self.gameStarted:
            return
        self.gameStarted = True
        params = self.getParams("all")
        object = {"object":"startGame"}
        out = dict( list( object.items() ) + list( params.items() ) )
        self.send2All(out)

        self.threadUpdate = threading.Thread(target=self.update())
        self.threadUpdate.daemon = True
        self.threadUpdate.start()

    def checkUsername(self,username,team):
        for _,player in self.players.items():
            if player.username == username and player.team == team:
                return False
        return True

    def checkTimeout(self):
        """
        timeout test
        """
        t = time.time() - self.tStart
        timeout = self.params.getParams("time")
        if t >= timeout:
            self.endGame("timeout")
            return False

    def checkVictory(self):
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
        for id,player in self.players.items():
            if player.status is not "kill":
                if id < 0:
                    tiduAlive += 1
                if id > 0:
                    tizefAlive += 1

        if tiduAlive == 0 and tiduZone == 0:
            self.endGame("tizefWin")
            return False
        if tizefAlive == 0 and tizefZone == 0:
            self.endGame("tiduWin")
            return False

    def e():
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
        if player.status != "playing":
            return
        if player.team == "tizef":
            team = "tizef"
        elif player.team == "tidu":
            team = "tidu"
        for index2,value2 in enumerate(self.teams[team]):
            if value2.status != "playing":
                continue
            d(self.debug,"test battle :", player.username, "of the team tidu",
                    "and",value2.username, "of the team tizef")
            if utils.distance(player.pos,value2.pos) <= self.params.getParams("radius"):
                d(self.debug,"beginning of a battle between :",
                    player.username, "of the team tidu",
                    "and",value2.username, "of the team tizef")

                tmpBattle = Battle(value2,player)
                player.startBattle(value2,tmpBattle)
                value2.startBattle(player,tmpBattle)
