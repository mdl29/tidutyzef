from TTClientConnection import *
from utils import *
import json

class Player (TTClientConnection):
    def __init__(self, parent, sock, addr):
        TTClientConnection.__init__(self,parent, sock, addr)

        self.pos = [0,0] # (latitude,longitude)
        self.username=""
        self.team=""
        self.status="none"  #none = waiting for the begining of the party
                        #playing
                        #fighting
                        #kill =  the player is kill and it's looking for a regen zone
                        #other =  not playing e.g admin
    def setStatus(self,status):
        self.status = status

    def __str__(self):
        return "username :" + self.username +" team :" + self.team

    def onReceive(self,msg):
        data = TTClientConnection.onReceive(self,msg)
        if not data:
            return

        if not self.username and not "username" in data:
            self.sendError(usernameNotSet)
            return
        """
        the case keyword doesn't exist in python, so, we use a dictionary of function to call the appropriated function
        we use lambda to call 2 function or to modify the number of args to pass to the function
        """
        try:
            fct = {"login" : lambda : self.login(data),
                    "logout" : lambda : self.onConnectionClose(),
                    "updatePos" : lambda : self.updatePos(data),
                    "msg" : lambda : self.msg(data),
                    "setParams" : lambda : self.setParams(data),
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
        for player in self.parent.client:
            if player.team and player.username:
                if not player.team in out:
                    out[player.team] = []
                out[player.team].append(player.username)
        self.send(out)

    def startGame(self):
        if self.team != "admin":
            return
        params = self.parent.getParams("all")
        object = {"object":"startGame"}
        out = dict( list( object.items() ) + list( params.items() ) )
        self.parent.send2All(out)
        self.parent.startGame()

    def getParams(self,data):
        if "params" in data:
            params = self.parent.getParams(data["params"])
            object = {"object":"params"}
            out = dict( list( object.items() ) + list( params.items() ) )
            self.send(out)

    def setParams (self,data):
        params = {}
        for _,key in enumerate(data):
            if key is not "object":
                params[key] = data[key]
        if (self.parent.setParams(params)):
            self.send({object:"paramReceived"})

    def getParams(self,data):
        if "params" in data:
            params = self.parent.getParams(data["params"])
            object = {"object":"params"}
            out = dict( list( object.items() ) + list( params.items() ) )
            self.send(out)

    def setParams (self,data):
        params = {}
        for _,key in enumerate(data):
            if key is not "object":
                params[key] = data[key]
        if (self.parent.setParams(params)):
            self.send({object:"paramReceived"})

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
                    if data["username"] == "admin":
                        self.status = "other"
                    self.username = data["username"]
                    self.team = data["team"]
                    self.parent.send2All({"object" : "newUser","username":self.username,"team":self.team})
                    self.send({"object" :"loged"})
            else:
                self.sendError(usernameAlreadySet)

    def msg (self,data):
        if "msg" in data:
            if "to" in data:
                for dest in data["to"]:
                    for client in self.parent.client:
                        if client.username==dest:
                            client.send({"object" : "msg", "from":self.username,"msg":data["msg"],"private":True})
            else:
                self.parent.send2All({"object" : "msg", "from":self.username,"msg":data["msg"],"private":False})

    def updatePos(self,data):
        self.pos = (data["lat"],data["lng"])
        self.parent.send2All({"object":"updatePos","from":self.username,"pos": self.pos,"team":self.team,"status":self.status})
        self.parent.checkBattle(self)

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

    def onConnectionClose(self):
        self.send({"object" :"logout","user":self.username})
        self.parent.send2All({"object" :"connection","user":self.username,"status":"logout"})
        super()
