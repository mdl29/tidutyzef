from utils import *

class Battle:
    def __init__(self,client1,client2):
        self.clients = [client1, client2]
        self.choice = ["",""]
        client1.setStatus("fighting")
        client2.setStatus("fighting")

    def play(self,client,data):
        if "choice" in data:
            if client is self.clients[0]:
                self.choice[0] = data["choice"]
            elif client is self.clients[1]:
                self.choice[1] = data["choice"]
            if self.choice[0] and self.choice[1]:
                sortie = self.analyse(self.choice[0], self.choice[1])
                if sortie == 1:
                    winner = self.clients[0].username

                elif sortie == 2:
                    winner = self.clients[1].username
                if winner:
                    out = {"object":"battle","winner":winner}
                    self.clients[0].endBattle(out)
                    self.clients[1].endBattle(out)
                else:
                    winner = "any"
                    out = {"object":"battle","winner":winner}
                    self.clients[0].send(out)
                    self.clients[1].send(out)

    def analyse(self,choix1, choix2):
        if "papier" in choix1:
            if "papier" in choix2:
                return 0
            if "ciseau" in choix2:
                return 2
            if "pierre" in choix2:
                return 1

        if "ciseau" in choix1:
            if "papier" in choix2:
                return 1
            if "ciseau" in choix2:
                return 0
            if "pierre" in choix2:
                return 2

        if "pierre" in choix1:
            if "papier" in choix2:
                return 2
            if "ciseau" in choix2:
                return 1
            if "pierre" in choix2:
                return 0
        else :
            return -1

