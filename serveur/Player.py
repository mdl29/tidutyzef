from TTWsHandler import *
from utils import *
import json
from Game import Game

class Player (TTWsHandler):
    def __init__(self,*args):
        self.ID=0
        self.pos = [0,0] # (latitude,longitude)
        self.username=""
        self.team=""
        self.status="none"  #none = waiting for the begining of the party
                        #playing
                        #fighting
                        #kill =  the player is kill and it's looking for a regen zone
                        #other =  not playing e.g admin
        TTWsHandler.__init__(self,*args)

    def open(self):
        pass

    def setStatus(self,status):
        self.status = status

    def __str__(self):
        return "username :" + self.username +" team :" + self.team

    def onMessage(self,data):
        #d(True, "Player.onMessage")
        if not self.username and not "username" in data:
            self.sendError(usernameNotSet)
            return
        """
        the case keyword doesn't exist in python, so, we use a dictionary of function to call the appropriated function
        we use lambda to call 2 function or to modify the number of args to pass to the function
        """
        try:
            fct = {"login" : lambda : self.login(data),
                    "logout" : lambda : self.close(),
                    "updatePos" : lambda : self.updatePos(data),
                    "chat": lambda : self.sendMsg(data),
                    "getParams" : lambda : self.getParams(data),
                    "startGame" : lambda : self.startGame(),
                    "getAllUsers" : lambda : self.getAllUsers(),
                    "choice" : lambda : self.setBattleChoice(data)
            }[data["object"]]
        except KeyError:
            self.sendError(unknowObject)
            return
        fct()# this execute the fonction which correspond whith the dict

    def setBattleChoice(self,data):
        try:
            self.battleSupervisor
        except NameError:
            return
        if "choice" in  data:
           self.battleSupervisor.play(self,data)

    def getAllUsers(self):
        out = {"object":"usersConnected"}
        for _,player in Game().players.items():
            if not player.team in out:
                out[player.team] = []
            out[player.team].append(player.username)
        self.send(out)

    def startGame(self):
        if self.team != "admin":
            return
        Game().startGame()

    def getParams(self,data):
        if "params" in data:
            params = Game().getParams(data["params"])
            object = {"object":"params"}
            out = dict( list( object.items() ) + list( params.items() ) )
            self.send(out)

    def setParams (self,data):
        params = {}
        for _,key in enumerate(data):
            if key is not "object":
                params[key] = data[key]
        if (Game().setParams(params)):
            self.send({object:"paramReceived"})

    def login (self,data):
        if "username" in data and "team" in data:          #set username
            if not self.username:
                if not Game().checkUsername(data['username'],data['team']):
                    self.error(usernameAlreadyUse)
                    return

                self.username = data["username"]
                self.team = data["team"]

                if True:#try:
                    self.ID = Game().addPlayer(self)
                else:#except Exception as ex:
                    d(self.debug, ex.args)

                Game().send2All({"object" : "newUser","username":self.username,"team":self.team})
                self.send({"object" :"logged"})
            else:
                self.sendError(usernameAlreadySet)

    def updatePos(self,data):
        #d(True, "Player.updatePos")
        self.pos = (data["lat"],data["lng"])
        Game().send2All({"object":"updatePos","from":self.username,"pos": self.pos,"team":self.team,"status":self.status})
        Game().addPlayerToBattle(self)
        Game().playerPositionUpdated()

    def sendMsg(self,data):
        Game().send2All({"object":"chat","from":self.username,"content":data["content"]})

    def startBattle(self,against,sup):
        self.send({"object" :"startBattle", "against" : against.username})
        self.status = "fighting"
        self.battleSupervisor = sup

    def endBattle(self,msg):
        if not "winner" in msg:
            return
        if msg ["winner"] is not self.username and msg["winner"] is not "any":
            self.status = "kill"
        else:
            self.status = "playing"
        self.send(msg)
        self.send({"object":"endBattle"})
        del self.battleSupervisor

    def on_close(self):
        d(self.debug, "on_close : ", self.username)
        Game().removePlayer(self.ID)
        Game().send2All({"object" :"connection","user":self.username,"status":"logout"})
