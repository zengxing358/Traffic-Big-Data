import math
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
def getgrid(lon1,lat1,lon2,lat2,accuracy):
    latStart = min(lat1, lat2)
    lonStart = min(lon1, lon2)
    deltaLon = accuracy * 360 / (2 * math.pi * 6371004 * math.cos((lat1 + lat2) * math.pi / 360))
    deltaLat = accuracy * 360 / (2 * math.pi * 6371004)
    lonsum=int((lon2-lon1)/deltaLon)+1
    latsum=int((lat2-lat1)/deltaLat)+1
    data=gpd.GeoDataFrame()
    LONCOL=[]
    LATCOL=[]
    geometry=[]
    HBLON1=[]
    HBLAT1=[]
    for i in range(lonsum):
        for j in range(latsum):
            HBLON = i*deltaLon + lonStart 
            HBLAT = j*deltaLat + latStart
            #把生成的数据都加入到前面定义的空list里面
            LONCOL.append(i)
            LATCOL.append(j)
            HBLON1.append(HBLON)
            HBLAT1.append(HBLAT)
            #生成栅格的Polygon形状
            #这里我们用周围的栅格推算三个顶点的位置，否则生成的栅格因为小数点取值的问题会出现小缝，无法完美覆盖
            HBLON_1 = (i+1)*deltaLon + lonStart
            HBLAT_1 = (j+1)*deltaLat + latStart 
            geometry.append(Polygon([
            (HBLON-deltaLon/2,HBLAT-deltaLat/2),
            (HBLON_1-deltaLon/2,HBLAT-deltaLat/2),
            (HBLON_1-deltaLon/2,HBLAT_1-deltaLat/2),
            (HBLON-deltaLon/2,HBLAT_1-deltaLat/2)]))
    #为geopandas文件的每一列赋值为刚刚的list
    data['LONCOL'] = LONCOL
    data['LATCOL'] = LATCOL
    data['HBLON'] = HBLON1
    data['HBLAT'] = HBLAT1
    data['geometry'] = geometry
    return data