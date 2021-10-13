
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from nonnegfac.nmf import NMF

result2 = pd.read_csv('H:/极客时间训练营/正式课程-资料/M14-共享单车利用率与解释因子/data/OD/od_select14.csv')
matrix=result2.pivot_table(index="BIKE_ID",columns="TownName_y",values="DATA_TIME",aggfunc="count")
matrix=matrix.fillna(0)
X=matrix.values
region = gpd.read_file('H:/极客时间训练营/正式课程-资料/M14-共享单车利用率与解释因子/data/shpData/basic_shp/shanghai_select_town_wgs84.shp')

def com3(n):
    W, H, info = NMF().run(X, n)
    dx=pd.DataFrame(H)
    dx['region'] = dx.apply(lambda x:np.argmax(x),axis=1)
    names = matrix.T.reset_index()['TownName_y']
    df_use = pd.concat([dx,names],axis=1)[['region','TownName_y']]
    df = region.merge(df_use,left_on='TownName',right_on='TownName_y')
    return df,info["final"]["rel_error"]

fig,ax=plt.subplots(3,4,figsize=(20,12))
lst=[]
cur=2
for i in range(3):
    for j in range(4):
        df,e=com3(cur)
        df.plot(ax=ax[i,j],column="region",cmap="tab20")
        ax[i,j].set_title(f"Rank={cur}",fontsize=20,fontfamily="Times New Roman")
        ax[i,j].axis("off")
        lst.append([cur,e])
        cur+=1
plt.tight_layout()

import numpy as np

def get_distance_from_point_to_line(point, line_point1, line_point2):
    #对于两点坐标为同一点时,返回点与点的距离
    if line_point1 == line_point2:
        point_array = np.array(point)
        point1_array = np.array(line_point1)
        return np.linalg.norm(point_array -point1_array )
    #计算直线的三个参数
    A = line_point2[1] - line_point1[1]
    B = line_point1[0] - line_point2[0]
    C = (line_point1[1] - line_point2[1]) * line_point1[0] + \
        (line_point2[0] - line_point1[0]) * line_point1[1]
    #根据点到直线的距离公式计算距离
    distance = np.abs(A * point[0] + B * point[1] + C) / (np.sqrt(A**2 + B**2))
    return distance

tmps=pd.DataFrame(lst)
tmps["dis"]=tmps[[0,1]].apply(lambda x:get_distance_from_point_to_line(list(x),list(tmps.iloc[0].values),list(tmps.iloc[-1].values)),axis=1)
bestrank=tmps.iloc[np.argmax(tmps["dis"]),0]

plt.figure(figsize=(10,10))
plt.plot([tmps.iloc[0,0],tmps.iloc[-1,0]],[tmps.iloc[0,1],tmps.iloc[-1,1]],ls="--",c="k")
plt.plot(tmps[0],tmps[1])
plt.scatter(tmps[0],tmps[1])
plt.scatter(tmps.iloc[np.argmax(tmps["dis"]),0],tmps.iloc[np.argmax(tmps["dis"]),1],marker="*",s=500,color="red")