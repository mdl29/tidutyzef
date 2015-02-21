import Params
import time
import threading
import utils
from zone import *
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
        self.positionUpdatedCond = threading.Condition()


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
        if self.admin:
            del self.admin

    def getPlayerByID(self,id):
        if id in self.players:
            return self.players[id]
        else:
            raise Exception("Player's ID {} don't exist".format(id))

    #def checkZones(self):
    #    for zone in self.zones:
    #        zone.update()

    def playerPositionUpdated(self):
        """
            Notify Game thread that a position has been updated.
        """
        d(True, "Position updated")
        self.positionUpdatedCond.acquire()
        self.positionUpdatedCond.notify()
        self.positionUpdatedCond.release()

    def update(self):
        self.tStart = time.time()
         
        while self.gameStarted:
            d(True, "while game started")
            
            #-- wait for position update
            self.positionUpdatedCond.acquire()
            self.positionUpdatedCond.wait()
            self.positionUpdatedCond.release()
            
            
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
        self.timer = threading.Timer(self.params.getParams("time"), endGameWithTime)
        # updating players status
        for _,player in self.players.items():
            player.setStatus("playing")

        self.gameStarted = True
        params = self.getParams("all")
        object = {"object":"startGame"}
        out = dict( list( object.items() ) + list( params.items() ) )
        self.send2All(out)
        self.threadUpdate = threading.Thread(target=self.update)
        self.threadUpdate.daemon = True
        self.threadUpdate.start()
    
    def endGameWithTime(self):
      endGame("temps écoulé")

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

        d(True, "nb Tidu Vivant : ", tiduAlive, "nb Tizef Vivant : ", tizefAlive)
        if tiduAlive == 0 and tiduZone == 0:
            self.endGame("tizefWin")
            return False
        if tizefAlive == 0 and tizefZone == 0:
            self.endGame("tiduWin")
            return False

    def checkZones(self):
            """
            zones test
            """
            pass
     #       for index,client in enumerate(self.client):
     #           if client.status is not "playing" or client.status is not "kill":
     #               continue
     #           for index,zone in enumerate(self.params.getParams(zones)):
     #               if utils.distance(zone.team,client.team) <= self.params.getParams("radius"):
     #                   zone.addPlayerInRadius(client)

    def getPlayersInTeam(self, teamName):
        """
        Return all players in a specified team
        """
        out = [];
        for k,player in self.players.items():
            if player.team == teamName:
                out.append(player)
        return out

    def checkBattle(self,player):
        d(True, "P1: ", player.status, " P2: ", player.status)
        if player.status != "playing":
            return
        
        if player.team == "tizef":
            aTeam = "tidu"
            team = self.getPlayersInTeam("tidu")

        elif player.team == "tidu":
            aTeam = "tizef"
            team = self.getPlayersInTeam("tizef")
            
        else:
            print(player)
        for player2 in team:
            d(True, "player.name: ", player2.username, " player.status: ", player2.status)
            if player2.status != "playing":
                continue
            d(True,"test battle :", player.username, "of the team ", player.team,
                    "and",player2.username, "of the team ", player2.team)
            d(True, "Positions : P1:", player.pos, " P2:", player2.pos)
            d(True, "Distance : ", utils.distance(player.pos,player2.pos), " -- Radius:", self.params.getParams("radius"))
            if utils.distance(player.pos,player2.pos) <= self.params.getParams("radius"):
                d(True,"beginning of a battle between :",
                    player.username, "of the team ", player.team,
                    "and",player2.username, "of the team ", player2.team)

                d(True, "P1: ", player.status, " P2: ", player2.status)
                
                tmpBattle = Battle(player2,player)
                player.startBattle(player2,tmpBattle)
                player2.startBattle(player,tmpBattle)
