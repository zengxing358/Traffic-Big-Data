import pandas as pd
import numpy as np
from nonnegfac.nmf import NMF


# V=pd.read_csv("H:/极客时间训练营/正式课程-资料/M14-共享单车利用率与解释因子/test.csv")
#
# W, H, info = NMF().run(V.values, 10)
# # print(W)
# # print(H)
# print(info["final"]["rel_error"])
# print(info)
import scipy.stats as st
# u=30
# g=2
# r=0
# for x in range(40,61):
#     r+=1/np.sqrt(2*np.pi)*(np.e**((-(x-u)**2)/(2*g**2)))
# print("{:.6f}".format(r))

print(st.norm.cdf(60,loc=30,scale=5)-st.norm.cdf(40,loc=30,scale=5))