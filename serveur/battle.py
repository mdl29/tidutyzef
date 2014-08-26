class battle:
	def __init__(self,client1,client2):
		self.clients = [client1, client2]
		self.choice = ["",""]
		client1.send({object:"startBattle",against:client2.__str__()})
		client2.send({object:"startBattle",against:client1.__str__()})
		client1.setStatus("fighting")
		client2.setStatus("fighting")		
		
	def play(self,client,data):
		if "choice" in data:
			if client is self.clients[0]:
				if client["client"] == "client1":
					self.choice = data["choice"]
			elif client["client"] == "client2":
					self.choice = data["choice"]
		
		if choice[0] and choice[1]:
			sortie = analyse(self, clients[1], clients[2])
			return sortie
		
		{object:"startBattle",against.__str__()}

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
