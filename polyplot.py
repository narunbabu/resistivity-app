from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

import numpy as np

def get_bound_index(v1darray):
    return np.where(v1darray[:-1] != v1darray[1:])[0]


npzfile=np.load('xyzlogs.npy.npz')
ulablesfile='tikamgarh_thck_labels.npy'

unique_lbls=np.load(ulablesfile)
xl,yl,zl,sec_logs=npzfile['arr_0'],npzfile['arr_1'],npzfile['arr_2'],npzfile['arr_3']
i=0
polygons=[]
for ul in unique_lbls[:1]:
    bounds=[]
    for j in range(len(sec_logs)):
        s=sec_logs[j].copy()
        s[s!=ul]=100 
        if(i==0):
            zs=zl[0],zl[get_bound_index(s)[-1]]
        elif(i==len(unique_lbls)-1):
            zs=zl[get_bound_index(s)[-1]],zl[-1]
        else:
            zbs=get_bound_index(s)
            zs=zl[zbs[0]],zl[zbs[-1]]
        bounds.append([xl[j],yl[j],zs[0],zs[1],ul])
    polygons.append(np.array(bounds))
    i +=1


x=np.append(polygons[0][:,0],polygons[0][:,0])
y=np.append(polygons[0][:,1],np.flipud(polygons[0][:,1]))
z=np.append(polygons[0][:,2],np.flipud(polygons[0][:,3]))

verts = [list(zip(x, y, z))]
# print(verts)
fig = plt.figure(figsize=(5,5))
ax = Axes3D(fig)
ax.add_collection3d(Poly3DCollection(verts), zs='z')
ax.set_xlim((min(x),max(x)))
ax.set_ylim((min(y),max(y)))
ax.set_zlim((min(z),max(z)))
ax.invert_zaxis()
# ax.scatter(x, y, z)
plt.show() 