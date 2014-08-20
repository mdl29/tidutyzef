import threading
from time import sleep

class Zone (threading.Thread):
    def __init__(self,pos,team):
        threading.Thread.__init__(self)
        self.daemon = True
        self.pos = pos
        self.team = team
        self.countdown = 0
        self.isStarted = False
        self.time2Kill = 10
        self.maxTime2Kill = 10
        self.keepAlive = threading.Event()
        self.start()

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

    def getTime2Kill(self)
        return self.time

    def run(self):
        self.keepAlive.set()
        while self.keepAlive.isSet():
            if time2Kill >= 0:
              if isStarted:
                    time2Kill = time2Kill - 0.1
                    sleep (0.1)

              else:
                    time2Kill = max (time2Kill + 0.1,maxTime2Kill)
                    sleep (0.1)

    def stop(self):
        self.keepAlive.clear()
