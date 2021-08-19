import numpy as np
from scipy.spatial import cKDTree
import itertools
from operator import itemgetter
import pandas as pd
import geopandas as gpd
def ckdnearest_point(pointsA,pointsB):
    nA=np.array(list(pointsA.geometry.apply(lambda x:(x.x,x.y))))
    nB=np.array(list(pointsB.geometry.apply(lambda x:(x.x,x.y))))
    btree=cKDTree(nB)
    dis,idx=btree.query(nA,k=1)
    res=pd.concat([pointsA.reset_index(drop=True),pointsB.loc[idx,pointsB.columns!="geometry"].reset_index(drop=True),
                  pd.Series(dis,name="dis")],axis=1)
    return res
def ckdnearest_line(pointsA,linsB):
    nA=np.concatenate([np.array(geom.coords) for geom in pointsA.geometry.to_list()])
    nB=[np.array(geom.coords) for geom in linsB.geometry.to_list()]
    B_idx=tuple(itertools.chain.from_iterable([itertools.repeat(i,x) for i,x in enumerate(list(map(len,nB)))]))
    nB=np.concatenate(nB)
    btree=cKDTree(nB)
    dis,idx=btree.query(nA,k=1)
    idx=itemgetter(*idx)(B_idx)
    res=pd.concat([pointsA.reset_index(drop=True),linsB.loc[idx,linsB.columns!="geometry"].reset_index(drop=True),
                  pd.Series(dis,name="dis")],axis=1)
    return res