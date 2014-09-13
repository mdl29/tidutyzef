class Params:
    def __init__(self):
        self.params = {"zones":[],"radius":10,"map":[0,0],"time":[10,60]}

    def setParams (self,params):
        for _,val in enumerate(params):
            if val == "zones":
                for _,zone in enumerate(params["zones"]):
                   if pos in zone and team in zone:
                        self.params[val] = Zone()
            if val == "map":
                self.params["map"][0] = params["map"]["lat"]
                self.params["map"][1] = params["map"]["lng"]
            elif val in self.params:
                self.params[val] = params[val]

    def getParams (self,params):
        out = {}
        if isinstance(params,str) or not params:
            if params == "all" or params == "" or not params:
                params = []
                for _,val in enumerate(self.params.keys()):
                    params.append(val)
            elif params == "zones":
                out ["zones"] = self.getAllZones()
            elif params in self.params:
                out = self.params[params]

        for _,val in enumerate(params):
            if val == "zones":
                out ["zones"] = self.getAllZones()
            elif val in self.params:
                out[val] = self.params[val]
        return out

    def getAllZones(self):
        out = []
        for _,zone in enumerate(self.params["zones"]):
            out.append(zone.__str__())
        return out

