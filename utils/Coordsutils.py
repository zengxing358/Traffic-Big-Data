def webMercator2lonlat(x,y):
    lonlat=[0]*2
    lon = x/20037508.34*180
    lat = y/20037508.34*180 
    lat= 180/math.pi*(2*math.atan(math.exp(lat*math.pi/180))-math.pi/2)
    lonlat[0] = lon 
    lonlat[1] = lat 
    return lonlat
