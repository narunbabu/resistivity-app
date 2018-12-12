import numpy as np
import matplotlib.pyplot as plt
from   mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
def add_polygons(ax,polysets,flip=True):
    for polygons in polysets:
        for k in range(len(polygons)):
            if len(polygons[k])>0:
                if flip:
                    x=np.array(polygons[k][:,1])
                    y=np.array(polygons[k][:,0])
                else:
                    x=np.array(polygons[k][:,0])
                    y=np.array(polygons[k][:,1])
                z=np.array(polygons[k][:,2])
                verts = [list(zip(x, y, z))]
                collection = Poly3DCollection(verts, linewidths=2, alpha=1)
                collection.set_facecolor(facies_colors[final_lbls[k]])
                ax.add_collection3d(collection,zs='z')
    return ax
facies_colors=np.load('facies_colors.npy')


E,N,Ele,allLoc_numbers=np.load('loc_info.npy')
final_lbls=np.load('final_lbls.npy')
fig = plt.figure(figsize=(15,5))
ax = Axes3D(fig)

# #wells not matching
# total_section=np.load('polysets3d.npy')

# for part_section in total_section:
#     ax=add_polygons(ax,part_section,flip=True)
# mywellset=np.load('mywellset_ele3d.npy')
# ax=add_polygons(ax,mywellset,flip=False)
# ax.set_xlim((78.6,79.6))
# ax.set_ylim((24.6,25.6))
# for i in range(1,len(allLoc_numbers)):
#     ax.text(N[i], E[i],-Ele[i],  '%s' % int(allLoc_numbers[i]), size=10, zorder=1, color='k') 


#wells matching
# polyset_file='polysets.npy'
polyset_file='polysets-new.npy'
total_section=np.load(polyset_file)

for part_section in total_section:
    ax=add_polygons(ax,part_section,flip=False)

# wellset_file='mywellset_ele.npy'
wellset_file='mywellset_ele-new.npy'
mywellset=np.load(wellset_file)
ax=add_polygons(ax,mywellset,flip=False)

# for part_section in total_section:
#     ax=add_polygons(ax,part_section,flip=False)
# ax=add_polygons(ax,mywellset,flip=True)
ax.set_xlim((78.6,79.25))
ax.set_ylim((24.6,25.6))

# ax.set_ylim((78.6,79.6))
# ax.set_xlim((24.6,25.6))
for i in range(1,len(allLoc_numbers)):
    ax.text(E[i], N[i],-Ele[i]-20,  '%s' % int(allLoc_numbers[i]), size=10, zorder=1, color='k') 
    # ax.text(N[i], E[i],-Ele[i]-20,  '%s' % int(allLoc_numbers[i]), size=10, zorder=1, color='k') 
            # ax.plot(x,y,z,'*')

# ax.set_xlim((min(x),max(x)))
# ax.set_ylim((min(y),max(y)))
# ax.set_zlim((min(z),max(z)))
# ax.set_xlim((min(x)-0.4,max(x)+.4))
# ax.set_ylim((min(y)-.4,max(y)+.4))



ax.set_zlim((-350,100))
# ax.plot(x,y,z,'*')
ax.invert_zaxis()
ax.view_init(elev=10., azim=150)
# ax.scatter(x, y, z)
plt.show()  