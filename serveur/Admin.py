from TTWsHandler import *
from Game import Game
from utils import *
import json

class Admin (TTWsHandler):
    def __init__(self,*args):
        TTWsHandler.__init__(self,*args)

    def open(self):
        try:
            self.ID = Game().setAdmin(self)
        except Exception as ex:
            d(self.debug, ex.args)

    def __str__(self):
        return "I'm the admin, the only one admin !! :"

    def onMessage(self,data):
        """
        the case keyword doesn't exist in python, so, we use a dictionary of function to call the appropriated function
        we use lambda to call 2 function or to modify the number of args to pass to the function
        """
        try:
            fct = { "logout" : lambda : self.close(),
                    "setParams" : lambda : self.setParams(data),
                    "getParams" : lambda : self.getParams(data),
                    "startGame" : lambda : self.startGame(),
                    "getAllUsers" : lambda : self.getAllUsers()
            }[data["object"]]
        except KeyError:
            self.sendError(unknowObject)
            return
        fct()# this execute the fonction which correspond whith the dict

    def getAllUsers(self):
        out = {"object":"usersConnected"}
        for _,player in enumerate(Game().players):
            if player.team and player.username:
                if not player.team in out:
                    out[player.team] = []
                out[player.team].append(player.username)
        self.send(out)

    def startGame(self):
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

    def on_close(self):
        Game().send2All({"object" :"connection","user":"Admin","status":"logout"})
        Game().unsetAdmin()
