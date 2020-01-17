from math import radians, cos, sin, asin, sqrt, fabs

EARTH_RADIUS = 6371
def haversine(point1, point2):
    """
    Calculate the great circle distance[in meters] between two points.
    on the earth(specified in decimal degrees).
    """
    # decimal to radians
    lon1, lat1, lon2, lat2 = map(radians, [point1[0], point1[1], point2[0],point2[1]])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2+cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    return c*EARTH_RADIUS


if __name__ == "__main__":
    print("野生动物园->坪山：%fm"%(haversine([113.973129, 22.599578],[114.3311032, 22.6986848])))
