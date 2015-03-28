import threading, utils
import time

class Zone (threading.Thread):
    id = 0
    def __init__(self,pos,team,radius):
        threading.Thread.__init__(self)
        self.daemon = True

        self._time = time.time()
        self.pos = pos
        self.team = team
        self.radius = radius
        self.isStarted = False
        self.ennemyInRadius = {"tidu": set(), "tizef": set() }
        self.killedInRadius = {}
        self.time2Kill = {"tidu" : 10, "tizef" : 10}
        self.maxTime2Kill = 10
        self.id = Zone.id
        Zone.id = Zone.id + 1

        self.keepAlive = threading.Event()
        self.start()

    def getDict(self):
        return {"id": self.id,"pos":self.pos, "team" : self.team,"time2chgTeam" : self.time2Kill}

    def addPlayerInRadius(self,player):
        print("addPlayerInRadius username: ", player.username)
        if player.team is not self.team:
            self.ennemyInRadius[player.team].add(player) # will add player only once (as it's a set) 
        elif player.status == "kill" and not player in self.playerInRadius:
            self.killedInRadius[player] = 10
            player.send({"object":"startRegen"})

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
        return self._time

    def run(self):
        self.keepAlive.set()

        import time
        while self.keepAlive.isSet():
            elapsedTime = time.time() - self._time
            """
            this part is use for the regen
            """
            for time,client in enumerate(self.killedInRadius):
                if utils.distance(self.pos,client.pos) > self.radius:
                    self.killedInRadius.pop(client)
                    client.send({"object":"endRegen","regen":"false"})

                if client.status is not "kill":
                    self.killedInRadius.pop(val)
                    continue

                time -= elapsedTime

                if time >= 0:
                    client.send({"object":"endRegen"})

            """
            this part is use for ennemis
            """
            for team in self.ennemyInRadius.keys():
                print("time2kill[", team, "] : ", self.time2Kill[team])
                if self.time2Kill[team] > 0:
                    if len(self.ennemyInRadius[team]) > 0:
                        self.time2Kill[team] = max(0,self.time2Kill[team]- elapsedTime)

                    else:
                        self.time2Kill[team] = min(self.time2Kill[team]+ elapsedTime ,self.maxTime2Kill)
                else:
                    self.__init__(self.pos,team,self.radius)

                if team == self.team:
                    continue
                for player in self.ennemyInRadius[team]:
                    if !val.isAlive: # joueur plus en vie
                        self.ennemyInRadius[team].remove(player)
                        print("Player (", player.username,"), not alive, removed")
                        continue

                    if player.status is not "playing":
                        continue

                    if utils.distance(self.pos,player.pos) > self.radius:
                        print("Player (", player.username,"), no longer in zone, removed")
                        self.ennemyInRadius[team].remove(player)


    def stop(self):
        self.keepAlive.clear()
