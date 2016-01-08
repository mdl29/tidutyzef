"""Some Maths fct for tidutizef"""
import math

def distance(origin, destination):
    """compute the distance between two coordonates"""
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # raduis of earth - > km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    tmp1 = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * \
            math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    tmp2 = 2 * math.atan2(math.sqrt(tmp1), math.sqrt(1-tmp1))
    return 1000 * radius * tmp2

