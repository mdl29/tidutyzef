from zone import *

class Params:
    def __init__(self,parent):
        self.params = {"zones":[],"radius":10,"map":[0,0],"time":600}
        self.parent = parent

    def setParams (self,params):
        if "radius" in params:
            self.params["radius"]=params["radius"]
            params["radius"].pop()
        for _,val in enumerate(params):
            if val == "zones":
                for _,zone in enumerate(params["zones"]):
                    if "pos" in zone and "team" in zone:
                        self.params["zones"].append(Zone(zone["pos"],zone["team"],self.params["radius"], self.parent))
            elif val == "map":
                self.params["map"][0] = params["map"]["lat"]
                self.params["map"][1] = params["map"]["lng"]
            elif val in self.params:
                self.params[val] = params[val]

    def getParam (self,param):
        if param == "zones":
        # We don't want to return Zone object, so we will get a simplified version of these objects
            return self.getAllZones()
        elif param in self.params:
            return self.params[param]
        else:
            raise Exception("param {} don't exist".format(param))

    def getParams (self,params='all'):
        out = {}
        if isinstance(params,str):
            if params == "all":
                for _,key in enumerate(self.params):
                    out[key] = self.getParam(key)
            else:
                out = self.getParam(params)
        return out

    def getAllZones(self):
        out = []
        for zone in self.params["zones"]:
            out.append(zone.__str__())
        return out

