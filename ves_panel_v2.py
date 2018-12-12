import numpy as np
import pandas as pd
import pickle
# %matplotlib inline
import matplotlib.pyplot as plt
import sys
sys.path.append('..')
from pickle_fns import *
import math
from scipy.interpolate import griddata,interp2d

def sliceLongString(string,limitLtrsperline):
    if len(string)<limitLtrsperline: return string
    nextstr=''
    lines=[]
    strs=string.split()
    for st in strs:
        nextstr += st+' '
        if len(nextstr)>limitLtrsperline:            
            lines.append(nextstr)
            nextstr=''
    return '\n'.join(lines)+'\n'+nextstr

def str_array2floats(strarray):
    floats=[]
    for s in strarray:
        try:
            floats.append(float(s))
        except:
            floats.append(np.nan)
    return floats
def get_lables(df,lith_dict):
    labels=[]
    for s in df['Interpreted Lithology'].values:
        for i in range(len(lith_dict)):
            if s in lith_dict[i]:
                if i in labels and i!=labels[-1]:
                    labels.append(i*10)
                else:
                    labels.append(i)
                break
    return labels
def make_same_numb_layers(master_l_thicknesses,lith_labels):
    layersinlocations=[len(l) for l in master_l_thicknesses]
    maxls=max(layersinlocations)
    j=-1
    for ml,ll in zip(master_l_thicknesses,lith_labels):
        j +=1
        if len(ml)<maxls:
            for i in range(maxls-len(ml)):
                ml.append(0)
                ll.append(-1)
                # ll.append(-1)
    loc_layers=np.array(master_l_thicknesses)
    return loc_layers,np.array(lith_labels)
# np.set_printoptions(precision=3,
# def get_lithdict():
#         #preparation of lith dictionary
#     fg_undersat=['Fractured Granite, may be under saturation',
#             'Fractured granite , may be under saturation',
#             'Fractured granite, may be under saturation',
#             'Fractured/weathered granite, may be under saturation']
#     gran= ['Granite',]
#     hard_gran=['Hard Granite', 'Hard granite', ]
#     high_weath_gr =['Highly Weathered granite','Highly weathered Granite', 'Highly weathered granite','Soil with kankars/Highly weathered Granite',
#             'Soil/Highly weathered Granite',]
#     soil_w_kankar= ['Overburden/top soil with kankars', 'Soil', 'Soil with kankars', 'Top Soil with kankars',
#             'Top soil', 'Top soil with kankars', 'Top soils with kankars',]
#     weather_gran=[ 'Weathered Granite', 'Weathered granite']
#     return {0:soil_w_kankar,1:high_weath_gr,2:weather_gran,3:gran ,4:fg_undersat,5:hard_gran,}

# vesdf,data_dfs=load_pkl('tikamgarh.pkl')
# vesnos=vesdf['VES No.'].values
# locations4panel=vesnos[0:nlocs]


# plot_VES_panel(vesdf,data_dfs,locations4panel)
def linefy(string):
    string.split()
def get_data4VES_panel(vesdf,data_dfs,lith_dict,locations4panel,max_strata_thickness=400):
    vesnos=list(vesdf['VES No.'].values)
    master_l_thicknesses=[]
    lith_labels=[]
    liths=[]
    
    lith=[]
    res=[]
    thicks=[]
    # E,N=vesdf.Easting.values.astype(np.float),vesdf.Northing.values.astype(np.float)

    elevations=str_array2floats(vesdf.RL.values)
    ves_data_dfs=[]
    loc_heads=[]
    eles=[]
    for loc in locations4panel:
        indx=vesnos.index(loc)
        a,b,c=tuple(vesdf[['Block','Location','VES No.']].values[indx])
        loc_heads.append('Block: {} \n Loc: {} \n VES: {}'.format(a,b,c) )
        ves_data_dfs.append(data_dfs[indx])
        eles.append(elevations[indx])
    master_l_thicknesses=[]
    lith_labels=[]
    for df in ves_data_dfs:
    #     print(df['Thickness(m)'].values.astype(np.float))
        layers_values=str_array2floats(df['Thickness(m)'].values)
        lastlayer_thickness=[max_strata_thickness-np.nansum(layers_values) if math.isnan(x) else x for x in layers_values]
#         print(lastlayer_thickness)
        master_l_thicknesses.append(list(lastlayer_thickness))
        lith_labels.append(list(get_lables(df,lith_dict) ))
        # lith_labels=np.append(lith_labels,df['lith_label'].values,axis=1)
        liths.append(df['Interpreted Lithology'].values)
        res.append(df['Resistivity(Ωm)'].values.astype(np.float))   
        thicks.append(str_array2floats(df['Thickness(m)'].values) ) 

    master_l_thicknesses,lith_labels=make_same_numb_layers(master_l_thicknesses,lith_labels)
    lithologies=np.array(liths)
    resistivities=np.array(res)
    thicknesses=np.array(thicks)
    lith_lbls=np.array(lith_labels)
    ths=np.array(master_l_thicknesses)
    nlocs=ths.shape[0]
    nlayers=ths.shape[1]+1
    vess=np.append(-np.array(eles),ths.T).reshape(nlayers,nlocs)
    return lithologies,resistivities,thicknesses,lith_lbls,vess,loc_heads

def plot_bars(ax,vesBarData,lith_lbls,loc_heads,fcolors,max_strata_thickness):
    nlayers,nlocs=vesBarData.shape
    onevess=vesBarData.T[0]
    _,N = vesBarData.shape
    inds = np.arange(N)    # the x locations for the groups
    width = 0.25      # the width of the bars: can also be len(x) sequence
    p1=[]
    bottom=vesBarData[0]
    for i in range(nlocs):
        onevess=vesBarData.T[i]
        # print(i)
        # print(onevess)
        # print('******************************************************')
        onelbs=lith_lbls[i]
        ind=inds[i]
#         print(onelbs)
        p1.append(ax.bar(ind+width/2,onevess[0], width,color=fcolors[onelbs[0] if onelbs[0]<10 else int(onelbs[0]/10)] ,ecolor='black'))
        bottom = onevess[0]
#         break
        
        for j in range(1,nlayers): 
            idx=onelbs[j-1] if onelbs[j-1]<10 else int(onelbs[j-1]/10)
            mycolor=fcolors[idx]
#             print(onevess[j],bottom,mycolor,onelbs[j-1],idx)
            p1.append(ax.bar(ind+width/2,onevess[j], width,bottom=bottom,color=mycolor))
            bottom += onevess[j]
    ax.set_ylabel('Depth (m)')
    ax.set_xticks(inds+width/2, minor=False)
    ax.set_xticklabels( loc_heads, minor=False)
    ax.xaxis.tick_top()
    x_coords=inds+width/2

    # Labels
    xlims=ax.get_xlim()
    ax.set_xlim(-0.5,inds[-1]+1)
    # ylims=ax.get_ylim()
    xlims=ax.get_xlim()
    xspacing=1.0/(nlocs+0.5)
    xwidth=(0.5+width)/(xlims[1]-xlims[0])
    # Placing L,R on both ends of panel

    tystarts=0.99-(np.array(vesBarData[0])-min(vesBarData[0]))/max_strata_thickness
    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    ax.text(0,0.99, "L", ha="center", va="center", size=20,transform=ax.transAxes,
            bbox=bbox_props)
    ax.text(1,0.99, "R", ha="center", va="center", size=20,transform=ax.transAxes,
            bbox=bbox_props)
    return x_coords,inds,width,bottom,tystarts

def hatch_patterns(nlayers,nlocs):
    patterns = ['-', '+', 'x', '\\', '*', 'o', 'O', '.',
                '-', '+', 'x', '\\', '*', 'o', 'O']
    patterns = np.array(patterns[0:nlayers]*nlocs)
    patterns=patterns.reshape(nlocs,nlayers)
    # for bar, pattern in zip(p1, patterns.T.ravel()):
    #     bar.set_hatch(pattern)
def add_lithoDescr(ax,vess,tystarts,lithologies,resistivities,thicknesses,lith_lbls,vesstrans,x_coords,inds,width,bottom,fcolors):
     # Labels
    xlims=ax.get_xlim()
    ax.set_xlim(-0.5,inds[-1]+1)
    # ylims=ax.get_ylim()
    xlims=ax.get_xlim()
    xspacing=1.0/(nlocs+0.5)
    xwidth=(0.5+width)/(xlims[1]-xlims[0])
    tx=0.0+xwidth
    for ty,ls,rs,thks,llb,vs,xc in zip(tystarts,lithologies,resistivities,thicknesses,lith_lbls,vesstrans,x_coords):
        cvs=np.cumsum(vs)   
        adder=10        
        
        # ty=0.95
        for i in range(len(ls)):       
            # textstr='R: '+str(int(rs[i]))+'- '+ls[i]+': '+str(ls[i])
            textstr = '\n'.join((
            r'Th: %.2f m; Res: %i $\Omega$-m' % (thks[i],rs[i], ),
            r'Lith: %s' % ( sliceLongString(ls[i],15), ),
            r'LithInd: %i' % (llb[i], )))
            idx=llb[i] if llb[i]<10 else llb[i]/10
            props = dict(boxstyle='round', facecolor=fcolors[int(idx)], alpha=0.5) #-0.6/nlocs
            ax.text(tx, ty, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props) 

            ty -=1/(len(ls)+1)

            adder+=20
        tx +=xspacing
    ax.set_yticks(np.arange(min(vess[0,:]), bottom+60, 20))
    # ax.legend(p1, layers,loc=4)
    ax.invert_yaxis()  
    
def plot_VES_panel(vesdf,data_dfs,lith_dict,locations4panel,figsize):
    max_strata_thickness=400
    lithologies,resistivities,thicknesses,lith_lbls,vess,loc_heads=get_data4VES_panel(vesdf,data_dfs,lith_dict,locations4panel,max_strata_thickness=max_strata_thickness)
    colors=['#C0C0C0','#D3D3D3',	'#00FFFF',	'#FFFF00','#FF0000',	'#00FF00',	'#008000',	'#0000FF','#808000','#800000',		'#008080',		'#000080',	'#FF00FF',	'#800080']
    nlayers,nlocs=vess.shape
    fcolors=colors[0:nlayers+1]  
    vesBarData = vess.copy()

    fig = plt.figure(figsize=(figsize))
    fig.suptitle('{}: VES Lithography correlation'.format(vesdf.iloc[0].Distt), fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)

    x_coords,inds,width,bottom,tystarts=plot_bars(ax,vesBarData,lith_lbls,loc_heads,fcolors,max_strata_thickness)

    hatch_patterns(nlayers,nlocs)


    add_lithoDescr(ax,vess,tystarts,lithologies,resistivities,thicknesses,lith_lbls,vess.T,x_coords,inds,width,bottom,fcolors)
    
    return plt


# [[0]]*(len(dvess)-len(vess))
def append_inequalarrays(aarray,barray): 
    a=list(aarray)
    a.extend(list(barray))
    return np.array(a)
def fill_missing(master_l_thicknesses,replace_val=0):
    layersinlocations=[len(l) for l in master_l_thicknesses]
    maxls=max(layersinlocations)
    new_m=[]
    for ml in master_l_thicknesses:
#         print(ml,maxls,[replace_val]*(maxls-len(ml)))
        if maxls>len(ml):
            ml=np.append(ml,[replace_val]*(maxls-len(ml)))
#             print(ml)
        new_m.append(ml)
    return np.array(new_m)

def plot_hibrid_VES_panel(vesdf,data_dfs,lith_dict,locations4panel,dvesdf,drill_dfs,dlith_dict,dlocations4panel):
    max_strata_thickness=400
    locations4panel=['112']
    lithologies,resistivities,thicknesses,lith_lbls,vess,loc_heads \
    = get_data4VES_panel(vesdf,data_dfs,lith_dict,locations4panel,max_strata_thickness=max_strata_thickness)
    dlithologies,dresistivities,dthicknesses,dlith_lbls,dvess,dloc_heads \
    = get_data4VES_panel(dvesdf,drill_dfs,dlith_dict,dlocations4panel,max_strata_thickness=max_strata_thickness)

    #merge dvess and vess
    if len(dvess)>len(vess):
        intvess=np.append(vess,[[0]*vess.shape[1]]*(len(dvess)-len(vess)),axis=0)
    mvess=np.append(intvess,dvess,axis=1)

    mlithologies=append_inequalarrays(lithologies,dlithologies)
    mresistivities=append_inequalarrays(resistivities,dresistivities)
    mresistivities =fill_missing(mresistivities)

    mthicknesses=append_inequalarrays(thicknesses,dthicknesses)
    mlith_lbls=append_inequalarrays(lith_lbls,dlith_lbls)
    mlith_lbls =fill_missing(mlith_lbls,replace_val=-1)
    mloc_heads=loc_heads
    mloc_heads.extend(dloc_heads)


    nlayers,nlocs=mvess.shape
    fcolors=colors[0:nlayers+1]  
    vesBarData = mvess.copy()

    fig = plt.figure(figsize=(figsize))
    fig.suptitle('{}: VES Lithography correlation'.format(vesdf.iloc[0].Distt), fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)

    x_coords,inds,width,bottom,tystarts=plot_bars(ax,vesBarData,mlith_lbls,mloc_heads,fcolors,max_strata_thickness=200)
    add_lithoDescr(ax,mvess,tystarts,mlithologies,mresistivities,mthicknesses,mlith_lbls,mvess.T,x_coords,inds,width,bottom,fcolors)
    return plt
    

    
if __name__ == '__main__':
    base_folder=r'D:\Ameyem Office\Projects\Electric surveys\Easwar files\Mahoba\\'
    vesdf,data_dfs=load_pkl(base_folder+'vesdf_datadf.pkl')
    # vesdf,data_dfs=load_pkl('tikamgarh.pkl')
    lith_dict=load_pkl(base_folder+'lith_dict.pkl')
    vesnos=vesdf['VES No.'].values
    # print(vesnos)
    nlocs=4
    locations4panel=['128' ,'129', '130', '131', '132','133'];file1='test1.jpg'
    locations4panel=['187', '184', '175', '146', '136', '148', '112', '122', '113', '158', '155', '164', '154'];file1='test2.jpg'
    figsize=4*len(locations4panel[0:nlocs]),10

    # locations4panel=['669','670', '668', '661', '662']
    plt=plot_VES_panel(vesdf,data_dfs,lith_dict,locations4panel[0:nlocs],figsize)
    plt.savefig(file1, dpi=150)
    plt.show()