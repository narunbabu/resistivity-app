import pickle
import numpy as np
from PyQt5.QtCore import QRect, QSize
from PyQt5.QtWidgets import (QAction, QApplication, QFrame,QFileDialog, QLabel,QLayout)
def get_closePointidx(pointxy, targetxys):
    from scipy import spatial
    myKDTree = spatial.KDTree(targetxys)
    distance,index=myKDTree.query(pointxy)
    return distance,index
def load_pkl(file):
    with open(file, 'rb') as f: 
        var = pickle.load(f)
        f.close()
    return var
def save_pkl(file,var):
    with open(file, 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump(var, f)
        f.close()
class ItemWrapper(object):
    def __init__(self, i, p):
        self.item = i
        self.position = p

#this is to digitize lithologies for better processing. It will be easier to plot them
def str_array2floats(strarray):
    floats=[]
    for s in strarray:
        try:
            floats.append(float(s))
        except:
            floats.append(np.nan)
    return floats


# np.array(lith_labels).shape
def merge_similar_layers(loc_layer,loc_lith_labels):
    res_layer=[]
    res_label=[]
    for a in np.unique(loc_lith_labels):
        single_layer_prop=0
        if a!=-1:
            single_layer_prop=0
            for n,l in zip(loc_lith_labels,loc_layer):
                if a==n:
                    single_layer_prop += l
            res_layer.append(single_layer_prop)
            res_label.append(a)
    return res_layer,res_label

# for processing purpose at all locations, same number of layers and labels prepared. 
def make_same_numb_layers(master_l_thicknesses,lith_labels):
    layersinlocations=[len(l) for l in master_l_thicknesses]
    maxls=max(layersinlocations)
    j=-1
    for ml in master_l_thicknesses:
        j +=1
        if len(ml)<maxls:
            for i in range(maxls-len(ml)):
                ml.append(0)
                lith_labels[j]=np.append(lith_labels[j],-1)
    loc_layers=np.array(master_l_thicknesses)
    return loc_layers,np.array(lith_labels)

#it is thought that if all the locations have layer thickness information according to sorted layers, it will be lot easier to 
#plot or process the information so the function for sorting single location and creating zero thickness layer for missing 
#layer
def get_sortedlayers4loc(mod_loc_layers,mod_loc_layer_lbls,unique_lbls):
    sorted_loc_layer=[]
    for ul in unique_lbls:
        sorted_loc_layer.append(0)
        for e,l in zip(mod_loc_layers,mod_loc_layer_lbls):
            if l==ul:
                sorted_loc_layer[-1]=e
#     sorted_loc_layer[-1]
    return sorted_loc_layer
def get_depths(thickness_layer_array,elevation):
    depths=[]
    d=-elevation   
    for e in thickness_layer_array:
        d += e
        depths.append(d)
    return depths

class BorderLayout(QLayout):
    West, North, South, East, Center = range(5)
    MinimumSize, SizeHint = range(2)

    def __init__(self, parent=None, margin=None, spacing=-1):
        super(BorderLayout, self).__init__(parent)

        if margin is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)
        self.list = []

    def __del__(self):
        l = self.takeAt(0)
        while l is not None:
            l = self.takeAt(0)

    def addItem(self, item):
        self.add(item, self.West)

    # def addWidget(self, widget, position):
    #     self.add(QWidgetItem(widget), position)

    def expandingDirections(self):
        return Qt.Horizontal | Qt.Vertical

    def hasHeightForWidth(self):
        return False

    def count(self):
        return len(self.list)

    def itemAt(self, index):
        if index < len(self.list):
            return self.list[index].item

        return None

    def minimumSize(self):
        return self.calculateSize(self.MinimumSize)

    def setGeometry(self, rect):
        center = None
        eastWidth = 0
        westWidth = 1
        northHeight = 0
        southHeight = 0
        centerHeight = 0

        super(BorderLayout, self).setGeometry(rect)

        for wrapper in self.list:
            item = wrapper.item
            position = wrapper.position
            if position == self.Center:
                center = wrapper

        centerHeight = rect.height() - northHeight - southHeight

        for wrapper in self.list:
            item = wrapper.item
            position = wrapper.position

            if position == self.West:
                item.setGeometry(QRect(rect.x() + westWidth,
                        northHeight, item.sizeHint().width()+20, centerHeight))   
                # print(item.sizeHint().width()) 

                westWidth += item.geometry().width() + self.spacing()


        if center:
            center.item.setGeometry(QRect(westWidth, northHeight,
                    rect.width() - eastWidth - westWidth, centerHeight))

    def sizeHint(self):
        return self.calculateSize(self.SizeHint)

    def takeAt(self, index):
        if index >= 0 and index < len(self.list):
            layoutStruct = self.list.pop(index)
            return layoutStruct.item

        return None

    def add(self, item, position):
        self.list.append(ItemWrapper(item, position))

    def calculateSize(self, sizeType):
        totalSize = QSize()

        for wrapper in self.list:
            position = wrapper.position
            itemSize = QSize()

            if sizeType == self.MinimumSize:
                itemSize = wrapper.item.minimumSize()
            else: # sizeType == self.SizeHint
                itemSize = wrapper.item.sizeHint()

            if position in (self.North, self.South, self.Center):
                totalSize.setHeight(totalSize.height() + itemSize.height())

            if position in (self.West, self.East, self.Center):
                totalSize.setWidth(totalSize.width() + itemSize.width())

        return totalSize