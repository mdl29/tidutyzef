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
            elif client["client"] == "client2":
                self.choice[1] = data["choice"]
            if choice[0] and choice[1]:
                sortie = analyse(self, clients[1], clients[2])
                return sortie
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

