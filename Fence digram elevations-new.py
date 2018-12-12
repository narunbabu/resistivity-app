import numpy as np
import matplotlib.pyplot as plt
from   mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
# # Plotly
# import plotly.plotly as py
# import plotly.tools as tls

from ves_panel_v3 import *
from HelperResL import *
def data_for_cylinder_along_z(center_x,center_y,radius,zrange=(-250,300)):
    z = np.linspace(zrange[0], zrange[1], 2)
    theta = np.linspace(0, 2*np.pi, 10)
    theta_grid, z_grid=np.meshgrid(theta, z)
    x_grid = radius*np.cos(theta_grid) + center_x
    y_grid = radius*np.sin(theta_grid) + center_y
    return x_grid,y_grid,z_grid
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
                # print(k,final_lbls)
                collection.set_facecolor(facies_colors[final_lbls[k]])
                ax.add_collection3d(collection,zs='z')
    return ax

base_folder=r'D:\Ameyem Office\Projects\Electric surveys\Easwar files\Mahoba\\'
vesdf,data_dfs=load_pkl(base_folder+'vesdf_datadf.pkl')
final_depths,unique_lbls,lith_dict_summay=np.load(base_folder+'final_depths_labes_summary.npy')

color_def={'top_soil':'#CCCCCC','high_weath_gr':'#FFFF80','weather_gran':'#ACACFF','granite':'#F07800',
           'frac_granite':'#FF99CC','hard_granite':'#B00600','agranite':'#AF99Cd','final_granite':'#B006A0'}

color_def={'top_soil':'#CCCCCC','weather_gran':'#ACACFF','granite':'#F07800',
           'frac_granite':'#FF99CC','hard_granite':'#B00600','agranite':'#AF99Cd','final_granite':'#B006A0'}
facies_colors=[color_def[l] for l in color_def]  
# facies_colors=np.load('facies_colors.npy')
# vesdf,data_dfs=load_pkl('tikamgarh.pkl')
E,N,Ele,allLoc_numbers=vesdf.Easting.values.astype(np.float),vesdf.Northing.values.astype(np.float), \
str_array2floats(vesdf.RL.values),vesdf['VES No.'].values

# E,N,Ele,allLoc_numbers=np.load('loc_info.npy')
final_lbls=[u if u<10 else np.uint8(u/10) for u in unique_lbls]
# final_lbls=np.load('final_lbls.npy')
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
# polyset_file='polysets-new.npy'

total_section=np.load(base_folder+'polysets.npy')

for part_section in total_section:
    ax=add_polygons(ax,part_section,flip=False)

# wellset_file='mywellset_ele.npy'

# wellset_file='mywellset_ele-new.npy'
# mywellset=np.load(wellset_file)
# ax=add_polygons(ax,mywellset,flip=False)

# for part_section in total_section:
#     ax=add_polygons(ax,part_section,flip=False)
# ax=add_polygons(ax,mywellset,flip=True)


# ax.set_xlim((78.6,79.25))
# ax.set_ylim((24.6,25.6))

# ax.set_ylim((78.6,79.6))
# ax.set_xlim((24.6,25.6))
for i in range(1,len(allLoc_numbers)):
    txt= ax.text(E[i], N[i],-Ele[i]-20,  '%s' % int(allLoc_numbers[i]),'z', size=9, zorder=0, color='k') 
    txt.set_clip_on(False)
    # ax.text2D(0.05, 0.95, "2D Text", transform=ax.transAxes)
    # ax.text2D(E[i], N[i],-Ele[i]-20,  '%s' % int(allLoc_numbers[i]), transform=ax.transAxes)
    # props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    # place a text box in upper left in axes coords
    # ax.text2D(E[i], N[i],-Ele[i]-20, '%s' % int(allLoc_numbers[i]), transform=ax.transAxes, fontsize=12,
    #         verticalalignment='top', bbox=props)

    # ax.plot([E[i],E[i]],  [N[i], N[i]],[-Ele[i]-20,100],'k',linewidth=10)

    Xc,Yc,Zc = data_for_cylinder_along_z(E[i],N[i],0.001,(-Ele[i]-5,300))
    ax.plot_surface(Xc, Yc, Zc, cmap='gray',alpha=1)
    # ax.text(N[i], E[i],-Ele[i]-20,  '%s' % int(allLoc_numbers[i]), size=10, zorder=1, color='k') 
            # ax.plot(x,y,z,'*')

ax.set_xlim((min(E),max(E)))
ax.set_ylim((min(N),max(N)))
# ax.set_zlim((min(z),max(z)))
# ax.set_xlim((min(x)-0.4,max(x)+.4))
# ax.set_ylim((min(y)-.4,max(y)+.4))



ax.set_zlim((-350,100))
# ax.plot(x,y,z,'*')
ax.invert_zaxis()
ax.view_init(elev=0., azim=120)
# ax.scatter(x, y, z)
plt.xlabel("Easting")
plt.ylabel("Northing")
# plt.zlabel("Depth")
# plotly_fig = tls.mpl_to_plotly(fig)
plt.show()  