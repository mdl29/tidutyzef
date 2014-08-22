#-*- coding:utf-8 -*-

from pyWebSocket import WebSocketServer, WebSocketClient
from TTWebSocketServer import *
import  json

usernameNotSet =  (0,"you should have an username and a team before any operation")
teamError = (1,"this team doesn't exist")
usernameAlreadyUse = (2,"username already in use in your team")
JSONError = (3,"the JSON can't be load")
unknowObject = (4,"the object is not set or isn't recognized")
usernameAlreadySet = ( 5,"you can't change your username")
userChgParams = (6, "you can't change params if you're not admin")
unknowParameter = (7, "the parameter you're asking for doesn't exist")

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
        WebSocketClient.__init__(self, parent, sock, addr)
        self.pos = (0,0) # (latitude,longitude)
        self.username=""
        self.team=""
        self.statuts=0  #0 = waiting for the begining of the party
                        #1 = playing
                        #2 = fighting
                        #3 = kill, the player is looking for a regen zone
                        #4 = not playing e.g admin
    def sendError(self,error): # errors codes are defined in the global scope
        self.send(json.dumps({"object":"error","errorCode":error[0],"desc":error[1]}))

    def onReceive(self,msg):
        """
        receive handler
        """
        if not msg:
            self.logout()
        try:
            data = json.loads(msg)
        except ValueError:
            print("data :",msg)
            self.sendError(JSONError)
            return
        if not self.username and not "username" in data:
            self.sendError(usernameNotSet)
            return
        """
        the case keyword doesn't exist in python, so, we use a dictionary of function to call the appropriated function
        we use lambda to call 2 function or to modify the number of args to pass to the function
        """
        print(data["object"])
        try:
            fct = {"login" : lambda : self.login(data),
                    "updatePos" : lambda : self.updatePos(data),
                    "msg" : lambda : self.msg(data),
                    "setParams" : lambda : self.setParams(data),
                    "getParams" : lambda : self.getParams(data),
                    "startGame" : lambda : self.startGame()
            }[data["object"]]
        except KeyError:
            self.sendError(unknowObject)
        fct()

    def startGame(self):
        if self.username != "admin":
            self.sendError(userChgParams)
            return
        for _,val in enumerate(self.parent.client):
            if val.statuts == 4:
                continue
            val.status = 1 

    def getParams(self,data):
        if "params" in data:
            if isinstance(data["params"],str) and data["params"] == "all":
                data["params"] = []
                for _,key in enumerate(self.parent.params):
                    data["params"].append(key)

            param2Send = {"object":"params"}
            for _,key in enumerate(data["params"]):
                if key in self.parent.params:
                    if key == "zones":
                        for index,val in enumerate(self.parent.params["zones"]):
                            param2Send[val.label]=val.__str__()
                    else:
                        param2Send[key]=self.parent.params[key]
                else:
                    self.sendError(unknowParameter)
                    print (key)
                    return
        self.send(json.dumps(param2Send))

                    

    def setParams (self,data):
        error = self.parent.setParams(data)
        if error == 0:
            return
        if error == 1:
            sendError(userChgParams)

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
                        self.status = 4
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
    def startBattle(self,against,sup):
        self.send(json.dumps({"object" :"battle", "against" : against.username}))
        self.status = 2
        self.battleSupervisor = sup
