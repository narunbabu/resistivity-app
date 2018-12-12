
# coding: utf-8

# In[174]:

# Modules and data loading
import numpy as np
import pandas as pd
import pickle
# get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import sys
sys.path.append('..')
from pickle_fns import *
import math
from scipy.interpolate import griddata,interp2d
from scipy import spatial
from numpy import ones,vstack
from numpy.linalg import lstsq
vesdf,data_dfs=load_pkl('tikamgarh.pkl')
E,N=vesdf.Easting.values.astype(np.float),vesdf.Northing.values.astype(np.float)

# plt.hist([len(v['Depth']) for v in volumelogs])
# lengths=[len(v['Lithology']) == len(v['Depth']) for v in volumelogs]
def clip_longer_logs(volumelogs):
    lengths=[len(v['Lithology'])  for v in volumelogs]
    ml=min(lengths)
    i=0
    for v in volumelogs:
        i +=1
        v['Depth']=v['Depth'][:ml]
        v['Lithology']=v['Lithology'][:ml]
    return volumelogs

# np.array(xi),sum(lengths)
def getasection(volumelogs,coords,x=78.8):
#     x=78.8
    coords=np.array(coords)
    closeid=np.argmin(abs(coords[:,0]-x),axis=0)
    sec_x=coords[closeid,0]
    # coords[:,0]-x
    x_index=np.where(coords[:,0]==sec_x)[0]
    sec_logs=[]
    for i in x_index:
    #     print(i)
        sec_logs.append(np.array(volumelogs[i]['Lithology'] ))
    return coords[x_index,0],coords[x_index,1],volumelogs[x_index[0]]['Depth'],np.array(sec_logs)
def gety(x,points):
    x_coords, y_coords = zip(*points)
    A = vstack([x_coords,ones(len(x_coords))]).T
    m, c = lstsq(A, y_coords)[0]
#     print("Line Solution is y = {m}x + {c}".format(m=m,c=c))
    return m*x+c
def get_indx_of_croockedline(coords,crooked_line):
    myKDTree = spatial.KDTree(coords)
    final_x=[]
    final_y=[]
    for i in range(1,len(crooked_line)):
        point_pair=np.array([crooked_line[i],crooked_line[i-1]])
    #     print(point_pair[:,0])

    #     
        sel_xi=xi[xi>=min(point_pair[:,0]) ]
        sel_xi=sel_xi[sel_xi<=max(point_pair[:,0])]
    #     break
        final_x.extend(sel_xi)
        final_y.extend(gety(sel_xi,point_pair))


    #get close_y index
    IND=[]
    for pt in zip(final_x,final_y):
        distance,index=myKDTree.query(pt)
        IND.append(index)
    return IND
def get_crooked_section(volumelogs,coords,xys):
#     x=78.8
    coords=np.array(coords)
    closeid=np.argmin(abs(coords[:,0]-x),axis=0)
    sec_x=coords[closeid,0]
    # coords[:,0]-x
    x_index=np.where(coords[:,0]==sec_x)[0]
    sec_logs=[]
    for i in x_index:
    #     print(i)
        sec_logs.append(np.array(volumelogs[i]['Lithology'] ))
    return coords[x_index,0],coords[x_index,1],volumelogs[x_index[0]]['Depth'],np.array(sec_logs)
def get_crooked_section(volumelogs,coords,xys):
#     x=78.8
    coords=np.array(coords)
    closeid=np.argmin(abs(coords[:,0]-x),axis=0)
    sec_x=coords[closeid,0]
    # coords[:,0]-x
    x_index=np.where(coords[:,0]==sec_x)[0]
    sec_logs=[]
    for i in x_index:
    #     print(i)
        sec_logs.append(np.array(volumelogs[i]['Lithology'] ))
    return coords[x_index,0],coords[x_index,1],volumelogs[x_index[0]]['Depth'],np.array(sec_logs)
def design_crooked_section(loc_array,vesdf):
    loc_coords=[]
    for loc in loc_array:
        loc_coords.append(vesdf[vesdf['VES No.']==str(loc)][['Easting','Northing']].values.astype(float))
    
    return loc_coords
def get_loc_lines(crooked_line,sec_logs):
    miny=min(crooked_line[:,1])
    maxy=max(crooked_line[:,1])
    perunit=len(sec_logs)/(maxy-miny)
    loc1x=[]
    loc1y=[]
    crooked_line
    for i in range(len(crooked_line)):
        lxval=(crooked_line[i,1]-miny)*perunit
        loc1x.append([lxval]*10)
        loc1y.append(list(range(0,400,40)))
    len(loc1x),len(loc1y),loc1x
    return loc1x,loc1y
def get_bound_index(v1darray):
    return np.where(v1darray[:-1] != v1darray[1:])[0]
def loggify(thicks_of_loc,labels,interval):
    rock_log=[]
    depth_log=[0]
    for layer,label in zip(thicks_of_loc,labels):
        for dt in np.arange(0,layer,interval):
            rock_log.append(label)
            depth_log.append(depth_log[-1]+interval)
    return {'Depth':depth_log[:-1],'Lithology':np.array(rock_log)}


# In[4]:

ulablesfile='tikamgarh_thck_labels.npy'
layers_outfile='tikamgarh_layers.npz'

npzfile=np.load(layers_outfile)
unique_lbls,lith_dict,xi,yi,layers=npzfile['arr_0'],npzfile['arr_1'],npzfile['arr_2'],npzfile['arr_3'],npzfile['arr_4']
nl,r,c=layers.shape
coords=[]
volumelogs=[]
for i in range(r):
    print(i,end=',')
    for j in range(c):
        lyrs=layers[:,i,j]
        volumelogs.append(loggify(lyrs,unique_lbls,interval=0.5))
        coords.append([xi[i],yi[j]])
volumelogs=clip_longer_logs(volumelogs)


# In[177]:

from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import gridspec
import matplotlib.colors as colors
from matplotlib.collections import PatchCollection
from matplotlib.patches import  Polygon
xl,yl,zl,sec_logs=getasection(volumelogs,coords,x=78.8)


color_def={'top_soil':'#CCCCCC','high_weath_gr':'#FFFF80','weather_gran':'#ACACFF','granite':'#F07800',
           'frac_granite':'#FF99CC','hard_granite':'#B00600','agranite':'#AF99Cd','final_granite':'#B006A0'}
facies_colors=[color_def[l] for l in color_def]
# i=5
def make_polygons(sec_logs,unique_lbls):
    polygons=[]
    for ul in unique_lbls:
        bounds=[]
    #     print(ul)
        for j in range(len(sec_logs)):
    #         print(j,end=',')
            s=  np.append(np.append(100,sec_logs[j]),100)
    #         print(s)
            s[s!=ul]=100 
            zbs=get_bound_index(s)
            if len(zbs)>0:
    #             print(zbs,len(zbs),end=',')
                if len(zbs)>1:
                    try:
                        zs=zl[zbs[0]],zl[zbs[1]-1]
                    except:
                        zs=zl[zbs[0]],zl[zbs[1]]
                else:
                    zs=zl[zbs[0]],zl[zbs[0]]
                bounds.append([xl[j],yl[j],zs[0],zs[1],ul])
        polygons.append(np.array(bounds))
#         i +=1
    return polygons
# cross_section_plot(sec_logs,yl)

def plot2dSectionFromPolys(polygons,yl):
    patches=[]
    for k in range(len(polygons)):
    #     print(k)
        if len(polygons[k])>0:
            x=np.append(polygons[k][:,0],polygons[k][:,0])
            y=np.append(polygons[k][:,1],np.flipud(polygons[k][:,1]))
            z=np.append(polygons[k][:,2],np.flipud(polygons[k][:,3]))
            polygon = Polygon(np.array([y,z]).T, True)
            patches.append(polygon)

    # fig, ax = plt.subplots()      
    f,ax=plt.subplots( figsize=(20, 5))
    colors = 100*np.random.rand(len(patches))
    p = PatchCollection(patches, alpha=0.4)
    p.set_array(np.array(colors))
    ax.add_collection(p)
    f.colorbar(p, ax=ax)
    ax.set_xlim(min(yl),max(yl))
    ax.set_ylim(0,200)
    ax.invert_yaxis()
    plt.show()
# polygons= make_polygons(sec_logs,unique_lbls)
# plot2dSectionFromPolys(polygons,yl)


# In[187]:

allLoc_numbers=vesdf['VES No.'].values.astype(np.int)
sections=[
    [658,664,657,660,659],[659,660,657,661,667],[663,664,658,668],
    [672,674,673],[667,661,660,659],[671,665,670]
]
sec_image_names=['SW-NE-Twoards North','SW-E-North crecent','N_S western flank','Southern three','S to N Near North','Estern Three']
polysets=[]
for section,sec_name in zip(sections,sec_image_names):
    crooked_line=design_crooked_section(section,vesdf)
    crooked_line=np.array(crooked_line).ravel().reshape(len(section),2)

#     basemap_plot(vesdf,crooked_line,sec_name)
    xycoords=[]
    sec_logs=[]
    IND=get_indx_of_croockedline(coords,crooked_line)
    for I in IND:
        xycoords.append(coords[I])
        sec_logs.append(np.array(volumelogs[I]['Lithology'] ))
    zl= volumelogs[IND[0]]['Depth']
    # xycoords,zl,sec_logs
    sec_logs=np.array(sec_logs)
    loc1x,loc1y=get_loc_lines(crooked_line,sec_logs)
    yl=np.array(xycoords)[:,1]
    polygons= make_polygons(sec_logs,unique_lbls)
#     plot2dSectionFromPolys(polygons,yl)
    polysets.append(polygons)

#     break
#     cross_section_plot(sec_logs,np.array(xycoords)[:,1],section,sec_name)

from   mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig = plt.figure(figsize=(15,5))
ax = Axes3D(fig)
for polygons in polysets:
    for k in range(len(polygons)):
#         print(k)
        if len(polygons[k])>0:
            x=np.append(polygons[k][:,0],polygons[k][:,0])
            y=np.append(polygons[k][:,1],np.flipud(polygons[k][:,1]))
            z=np.append(polygons[k][:,2],np.flipud(polygons[k][:,3]))

            verts = [list(zip(x, y, z))]
            # print(verts)
            # ax.add_collection3d(Poly3DCollection(verts), zs='z')
            # collection = Poly3DCollection(poly3d, linewidths=1, alpha=0.2)

            collection = Poly3DCollection(verts, linewidths=1, alpha=0.7)
        #     face_color = [0.5, 0.5, 1] # alternative: matplotlib.colors.rgb2hex([0.5, 0.5, 1])
            collection.set_facecolor(facies_colors[k])
            ax.add_collection3d(collection,zs='z')

# ax.set_xlim((min(x),max(x)))
# ax.set_ylim((min(y),max(y)))
# ax.set_zlim((min(z),max(z)))
# ax.set_xlim((min(x)-0.4,max(x)+.4))
# ax.set_ylim((min(y)-.4,max(y)+.4))
ax.set_xlim((78,79.5))
ax.set_ylim((24.6,25.6))
ax.set_zlim((0,200))

ax.invert_zaxis()
# ax.view_init(elev=10., azim=170)
# ax.scatter(x, y, z)
plt.show()       
    


# In[50]:

def cross_section_plot(sec_logs,yl):
    color_def={'top_soil':'#CCCCCC','high_weath_gr':'#FFFF80','weather_gran':'#ACACFF','granite':'#F07800',
               'frac_granite':'#FF99CC','hard_granite':'#B00600'} #,'agranite':'#AF99Cd','final_granite':'#B006A0'

    lith_label_def={0:'Top soil/w kankar',1:'Highly weath. Granite',2:'Weath. Granite',3:'Granite' ,4:'Und.Sat Frac. Granite',5:'Hard Granite',}
    facies_colors=[color_def[l] for l in color_def]
    facies_labels=[lith_label_def[l] for l in lith_label_def]
    # facies_colors[0:len(final_lbls)],facies_colors[0:len(unique_lbls)],len(final_lbls),len(unique_lbls),final_lbls,unique_lbls
    f,ax=plt.subplots(nrows=1, ncols=2, figsize=(20, 5))
    gs = gridspec.GridSpec(1, 2, width_ratios=[15,1]) 
    ax[0] = plt.subplot(gs[0])
    ax[1] = plt.subplot(gs[1])
    # cmap_facies = colors.ListedColormap( np.array(facies_colors)[final_lbls], 'indexed')
    cmap_facies = colors.ListedColormap( facies_colors[0:len(unique_lbls)], 'indexed')

    im=ax[0].imshow(sec_logs.T, interpolation='none', aspect='auto',
                            cmap=cmap_facies,vmin=0,vmax=6)
    trc_space=(max(yl)-min(yl))/len(sec_logs)
    ntraces=50
    tentrcspace=round(1000*trc_space*ntraces)/1000

    xticks=np.arange(round(min(yl)*100)/100,max(yl),tentrcspace)
    ind=np.arange(0,len(sec_logs),ntraces)
    ax[0].set_xlim(-10,len(sec_logs)+10)
    ax[0].set_xticks(ind)
    ax[0].set_xticklabels(xticks)
#     for lx,ly,l in zip(loc1x,loc1y,locations):
#         ax[0].plot(lx,ly,'k')
#         ax[0].annotate(l, xy=(lx[0]-3, ly[0]-1))

    # ax[0].set_xticks(ind)
    ax[0].set_yticklabels(np.arange(-25,200,25))
    # ax[0].set_xlim(min(yl),max(yl))
    divider = make_axes_locatable(ax[-1])
    # ax[1].set_ticklabels('')
    ax[-1].axis('off')
    cax = divider.append_axes("right", size="100%", pad=0.1)
    cbar=plt.colorbar(im, cax=cax)
    #     cbar.set_label((11*' ').join(facies_labels[::-1]))
    cbar.set_ticks(np.arange(0.5,6,1)); 
    # cbar.ax.set_xticklabels('')
    cbar.ax.invert_yaxis() 
    cbar.ax.set_yticklabels(facies_labels)
    plt.show()
#     f.savefig(image_name+'_vsection.png')

