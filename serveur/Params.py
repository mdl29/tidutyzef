from zone import *

class Params:
    def __init__(self,parent):
        self.params = {"zones":[],"radius":10,"map":[0,0],"time":[10,60]}
        self.parent = parent

    def setParams (self,params):
        if "radius" in params:
            self.params["radius"]=params["radius"]
            params["radius"].pop()
        for _,val in enumerate(params):
            if val == "zones":
                for _,zone in enumerate(params["zones"]):
                    if "pos" in zone and "team" in zone:
                        self.params["zones"].append( Zone(zone["pos"],zone["team"],self.params["radius"], self.parent) )
            elif val == "map":
                self.params["map"][0] = params["map"]["lat"]
                self.params["map"][1] = params["map"]["lng"]
            elif val in self.params:
                self.params[val] = params[val]

    def getParams (self,paramName):
        paramsForJSON = {}
        for k,v in self.params.items():
            if k == "zones":
                paramsForJSON[k]=self.getAllZones()
            else:
                paramsForJSON[k]=v
            
        return paramsForJSON[paramName] if (paramName in paramsForJSON) else paramsForJSON

    def getAllZones(self):
        out = []
        for zone in self.params["zones"]:
            out.append(zone.getDict())
        return out

