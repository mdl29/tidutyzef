import threading, utils
from time import sleep

class Zone (threading.Thread):
    def __init__(self,label,pos,team,parent):
        threading.Thread.__init__(self)
        self.daemon = True
        self.pos = pos
        self.parent = parent
        self.team = team
        self.isStarted = False
        self.label = label
        self.ennemyInRadius = []
        self.time2Kill = 10
        self.maxTime2Kill = 10
        self.keepAlive = threading.Event()
        self.start()

    def __str__(self):
        return [self.pos,self.team,self.time2Kill]

    def addEnnemyInRadius(self,client):
        self.ennemyInRadius.append(client)

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
            for index,val in enumerate (self.ennemyInRadius):
                if not val:
                    self.ennemyInRadius.pop(index)
                    continue
                if utils.distance(self.pos,val.pos) > parent.params["radius"]:
                    self.ennemyInRadius.pop(index)

            if self.time2Kill > 0:
              if len(self.ennemyInRadius) > 0:
                    self.time2Kill = self.time2Kill - 0.1
                    sleep (0.1)

              else:
                    self.time2Kill = min(self.time2Kill + 0.1,self.maxTime2Kill)
                    sleep (0.1)

    def stop(self):
        self.keepAlive.clear()

