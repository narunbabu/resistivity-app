
from matplotlib.mlab import prctile_rank
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
import numpy as np
import sys
sys.path.append('..')
from pickle_fns import *
file="D:\AI-ML\census\IND_adm\IND_adm2"

fig=plt.figure(figsize=(12,12),dpi=80, facecolor='w', edgecolor='k')
map= Basemap()
shp_info=map.readshapefile(file, 'IND_adm2')
for info, lightning in zip(map.IND_adm2_info, map.IND_adm2):
    if(info['NAME_2']=='Tikamgarh'):
        print(info['NAME_2'])
        x, y = zip(*lightning) 
        break
coords=np.array(lightning)

lonpt, latpt = map(coords[:,0],coords[:,1],inverse=True)

vesdf,data_dfs=load_pkl('tikamgarh.pkl')
labels=['Block', 'Date', 'Direction of Schlumberger Array', 'Distt',  
               'Geology','Location', 'RL', 'VES No.', 'Water Table']
d4plots=vesdf['Location'].values
E,N= vesdf.Easting.values.astype(np.float),vesdf.Northing.values.astype(np.float)
divfac=4
lllon,urlon,lllat,urlat=np.floor(divfac*min(lonpt))/divfac,np.ceil(divfac*max(lonpt))/divfac,np.floor(divfac*min(latpt))/divfac,np.ceil(divfac*max(latpt))/divfac



map= Basemap(llcrnrlon=lllon,llcrnrlat=lllat,urcrnrlon=urlon,urcrnrlat=urlat,resolution = 'l', epsg=24379)
shp_info=map.readshapefile(file, 'IND_adm2')
ix,iy=map(x, y)
map.plot(ix, iy, marker=None,color='g')
No = len(coords[:,0])
area = 4 * np.ones(No)
# polyx,polyy=map(coords[:,0],coords[:,1])
# plt.scatter(polyx,polyy, s=area, marker='.',color='lightgreen')
px,py=map(E,N)


# lon = urlon-0.6
# lat = urlat-0.6
# x1,y1 = map(lon, lat)
# x2, y2 = map(lon+0.5,lat+0.5)

# plt.arrow(x1,y1,x1,y2,fc="k", ec="k", linewidth = 4, head_width=1000, head_length=1000)
# map.drawmapboundary()
map.drawmapscale(78.50, 24.5, 0, 0, 40)
# map.drawarrow()
parallels =np.arange(24.2, 25.8,0.4)
# labels = [left,right,top,bottom]
map.drawparallels(parallels,labels=[False,True,True,False])
meridians =  np.arange(78.2, 79.6,0.4)
map.drawmeridians(meridians,labels=[True,False,False,True])
map.drawmapboundary(fill_color='grey')
plt.scatter(px,py,s=100, marker='o',c='r')
for i, txt in enumerate(d4plots):
        plt.annotate(txt, (px[i]+0.01, py[i]+0.01))
plt.show()

fig.savefig('map.png')