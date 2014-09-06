class Params:
    def __init__(self):
        self.params = {"zones":[],"radius":10,"mapCenter":[0,0]}

    def setParams (self,params):
        for _,val in enumerate(params):
            if val == "zones":
                for _,zone in enumerate(params["zones"]):
                   if pos in zone and team in zone:
                        self.params[val] = Zone()
            elif self.params[val]:

                out[val] = self.params[val]

    def getParams (self,params):
        out = {}

        if isinstance(params,str) or not params:
            if params == "all" or params == "" or not params:
                params = []
                for _,val in enumerate(self.params.keys()):
                    params.append(val)
            elif params == "zones":
                out ["zones"] = self.getAllZones()
            elif self.params[params]:
                out [params] = self.params[params]

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

