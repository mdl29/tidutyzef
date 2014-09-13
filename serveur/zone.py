import threading, utils
from time import sleep
import time

class Zone (threading.Thread):
    id = 0
    def __init__(self,pos,team,radius,parent) :
        threading.Thread.__init__(self)
        self.daemon = True

        self._time = time.time()
        self.pos = pos
        self.parent = parent
        self.team = team
        self.isStarted = False
        self.ennemyInRadius = {}
        self.killedInRadius = {}
        self.time2Kill = 10
        self.maxTime2Kill = 10
        self.id = id
        id = id + 1

        self.keepAlive = threading.Event()
        self.start()

    def __str__(self):
        return {"id": self.id,"pos":self.pos, "team" : self.team,"time2chgTeam" : self.time2Kill}

    def addPlayerInRadius(self,client):
        if client.team is not self.team:
            self.ennemyInRadius.add(client)
        elif client.status == "kill" and not client in self.playerInRadius:
            self.killedInRadius[client] = 10
            client.send({"object":"startRegen"})

    def setPosition(self,pos):
        self.pos = pos

    def getPosition(self):
        return self.pos

    def setAppartenance(self,team):
        self.team = team

    def getAppartenance(self):
        return self.team

    def setTime2Kill(self,time):
        self.time2Kill = time

    def getTime2Kill(self):
        return self.time

    def run(self):
        self.keepAlive.set()

        while self.keepAlive.isSet():
            elapsedTime =  time.time() - self._time

            """
            this part is use for the regen
            """
            for time,client in enumerate(self.playerInRadius):
                if not client.isAlive:
                    self.playerInRadius.pop(client)
                if utils.distance(self.pos,client.pos) > self.radius:
                    self.playerInRadius.pop(client)
                    client.send({"object":"endRegen","regen":"false"})

                if client.status is not "kill":
                    self.playerInRadius.pop(val)
                    continue

                time -= elapsedTime

                if time >= 0:
                    client.send({"object":"endRegen"})

            """
            this part is use for ennemis
            """
            for val in self.ennemyInRadius:
                if val.isAlive:
                    self.ennemyInRadius.remove(val)
                    continue

                if val.status is not "playing":
                    continue

                if utils.distance(self.pos,val.pos) > self.radius:
                    self.ennemyInRadius.remove(val)

            if self.time2Kill > 0:
              if len(self.ennemyInRadius) > 0:
                    self.time2Kill = self.time2Kill - elapsedTime

              else:
                    self.time2Kill = min(self.time2Kill + elapsedTime ,self.maxTime2Kill)

            self._time = time.time()

    def stop(self):
        self.keepAlive.clear()

