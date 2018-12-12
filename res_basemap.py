# %matplotlib inline
from matplotlib.mlab import prctile_rank
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap

file="D:\AI-ML\census\IND_adm\IND_adm2"

import numpy as np
import pandas as pd
import pickle
import sys
sys.path.append('..')
from pickle_fns import *

vesdf,data_dfs=load_pkl('tikamgarh.pkl')
E,N=vesdf.Easting.values.astype(np.float),vesdf.Northing.values.astype(np.float)



map= Basemap(llcrnrlon=68.,llcrnrlat=5.5,urcrnrlon=98.5,urcrnrlat=35.5,resolution = 'l', epsg=24378)

# ind= Basemap(llcrnrlon=70.,llcrnrlat=15,urcrnrlon=85,urcrnrlat=25,resolution = 'l', epsg=24378)
# map = Basemap(projection='ortho',lat_0=20, lon_0=60)

# map = Basemap(projection='tmerc',
# lat_0=15., lon_0=78.,llcrnrlon=60.,
# llcrnrlat=6.5,
# urcrnrlon=98.5,
# urcrnrlat=45.5)

# ind = Basemap(llcrnrlon=70.,llcrnrlat=6.,urcrnrlon=90.,urcrnrlat=11.,
#              resolution='i', projection='tmerc', lat_0 = 39.5, lon_0 = 1)
# # llcrnrlon=3.75,llcrnrlat=39.75,urcrnrlon=4.35,urcrnrlat=40.15
shp_info=map.readshapefile(file, 'IND_adm2')
# # x, y = zip(*ind.IND_adm0)
# # for item in ind.IND_adm0_info:
# #     print(item)
# map.drawcoastlines()
map.drawcoastlines()
x,y=map(E,N)
# map.fillcontinents()
plt.plot(x,y,'*')
plt.show()