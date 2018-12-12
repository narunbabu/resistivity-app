from PyQt5.QtCore import QRect, QSize, QDir, Qt,QPointF,QRectF
# from PyQt5.QtWidgets import (QApplication, QFrame, QLabel, QLayout,
#         QTextBrowser, QWidget, QWidgetItem)
from PyQt5.QtGui import QImage, QPainter, QPalette, QPixmap, QColor

from PyQt5.QtWidgets import (QAction, QApplication, QFrame,QFileDialog, QLabel,QLayout,
        QMainWindow, QMenu, QMessageBox, QScrollArea, QSizePolicy,QInputDialog,QListWidgetItem,
        QPushButton,QLineEdit,QListWidget,QGridLayout,QWidget,QGraphicsItem ,QWidgetItem,QTextBrowser)

import pyqtgraph as pg
import numpy as np
import pandas as pd
# import sys
# sys.path.append('..')
from HelperResL import *


class myListWidget(QListWidget):
    
   def Clicked(self,item):
      QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())


class ImageViewer(QMainWindow):
    curve=[]
    Image=[]
    E=[]
    N=[]
    Ele=[]
    last_point=[]
    profile_ves=[]
    profiles=[]
    listitem=[]
    profiletobeselected=False
    imfolder=r"D:\Ameyem Office\Geoservices\Digitizer\\"
    
    base_folder=r'D:\Ameyem Office\Projects\Electric surveys\Easwar files\jalaun\\'
    base_folder=r'D:\Ameyem Office\Projects\Electric surveys\Easwar files\Mahoba\\'
    
    zoom_fact=1
    fileName=''
    pick_type='digitize'
    depth_pix_lims=[]
    prop_pix_lims=[]
    def __init__(self):
        super(ImageViewer, self).__init__()

        self.createActions()
        self.createMenus()
        self.resize(800, 600)
        win = QWidget()
        self.setCentralWidget(win)
        # creates plot
        self.plot = pg.PlotWidget(name="VES Locations") 
        layout = BorderLayout()
        layout.add(QWidgetItem(self.plot), BorderLayout.Center)
        # List items
        self.list_w = QListWidget()
        self.listitem.append(QListWidgetItem('Welcome to ResLayer!!!'))
        self.list_w.setFrameStyle(QFrame.Box | QFrame.Raised)
        layout.add(QWidgetItem(self.list_w), BorderLayout.West)
        win.setLayout(layout)
        self.list_w.addItem(self.listitem[0])


        self.setWindowTitle("Border Layout")

        mypen = pg.mkPen('y', width=1)
        


        vesdf,data_dfs=load_pkl(self.base_folder+'vesdf_datadf.pkl')
        try:
            self.boundaries=load_pkl(self.base_folder+'boundaries.pkl')
        except:
            self.boundaries=[]
        try:
            self.profiles=load_pkl(self.base_folder+'profiles.pkl')
            # print(self.profiles)
            for profile in self.profiles:
                self.listitem.append(QListWidgetItem('Profile: '+'-'.join([p for p,q in profile])))
                self.list_w.addItem(self.listitem[-1])
        except:
            self.profiles=[]
        
        self.VES,self.E,self.N,self.Ele,self.block=vesdf['VES No.'].values,vesdf.Easting.values.astype(np.float), \
        vesdf.Northing.values.astype(np.float), \
        str_array2floats(vesdf.RL.values),vesdf.Block.values
        
        
        
        self.plot.setLabel('left', "Northing", units='deg')
        self.plot.setLabel('bottom', "Easting", units='deg')
        self.plot.showGrid(x=1, y=1, alpha=None)
        self.plot.showAxis('right')
        self.plot.showAxis('top')
        self.plot.getViewBox().setAspectLocked(True)
        # self.curve = pg.ScatterPlotItem(size=20, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
        # spots = [{'pos': j, 'data': 1} for j in zip(self.E,self.N)] 
        # self.curve.addPoints(spots)        

        self.curve = self.plot.plot(x=self.E, y=self.N, size=10, pen=pg.mkPen(None),  symbol='o') #brush=pg.mkBrush(255, 100, 255, 120),pen=None,
        #district and block boundaries
        if len(self.boundaries)>0:
            for b in self.boundaries:
                self.plot.plot(x=[g for g in b[0]], y=[g for g in b[1]])
        self.plot.addItem(self.curve)
        # labels=['{}-{}'.format(ves,blk) for ves,blk in zip(self.VES,self.block)]
        self.plot_labels(self.plot,self.E,self.N,self.VES,self.block)
        self.curve.scene().sigMouseMoved.connect(self.onMouseMoved)

        self.curve.scene().sigMouseClicked.connect(self.createVESprofile)



    def plot_labels(self,plot,xarray,yarray,labels,blocks):
        blocks=[b.upper() for b in blocks]
        colors=['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        colors=['#C0C0C0','#D3D3D3','#FF0000',	'#00FFFF',	'#FFFF00',	'#00FF00',	'#008000',	'#0000FF','#808000','#800000',		'#008080',		'#000080',	'#FF00FF',	'#800080']
        ublocks=np.unique(blocks)
        i=0
        for x,y,l,blk in zip(xarray,yarray,labels,blocks):
          
            cidx=np.where(ublocks==blk)[0][0]
            self.annotate(plot,x,y,colors[cidx],l)

    def annotate(self,plot,x,y,color,label,border=None,angle=0,fsize=8):
        txt='<div style="text-align: center"><span style="color: %s;font-size:%spt;">%s</span></div>'%(color,fsize,label)
        t=pg.TextItem( html=txt, anchor=(-0.1, 1.0), border=border, fill=None, angle=10, rotateAxis=None)
        t.setPos(x, y)
        plot.addItem(t)
    def onMouseMoved(self, point):
        # print(point)
        self.last_point = self.plot.plotItem.vb.mapSceneToView(point)
        self.statusBar().showMessage("Easting:{} Northing:{}".format(self.last_point.x(), self.last_point.y()))
    def onClick(self,event):
        # items = self.plot.scene().items(event.scenePos())
        newPos = self.plot.mapToScene(int(event.pos()[0]) ,int(event.pos()[0]) )
        # print(event.pos(),newPos)
        return self.plot.plotItem.vb.mapSceneToView(newPos)


    def createVESprofile(self,event):    

        coords=[[xi,yi] for xi,yi in zip(self.E,self.N)]
        dist,idx=get_closePointidx([self.last_point.x(),self.last_point.y()], coords)
        # self.list_w.addItem(self.VES[idx])
        self.listitem[0].setText('Selected VES No: ' +self.VES[idx])
        
        # print self.list_w.currentRow()
        # print (self.list_w.currentItem().text())
        # self.list_w.currentItem().text += self.VES[idx]
        if self.profiletobeselected:
            if self.VES[idx] not in [p for p,q in self.profile_ves]:
                self.profile_ves.append((self.VES[idx],coords[idx]))
            if len(self.profile_ves)==1:
                self.listitem.append(QListWidgetItem('Profile: '+self.profile_ves[0][0]))
                self.list_w.addItem(self.listitem[-1])
                
            if len(self.profile_ves)>1:
                profx=[b[0] for a,b in self.profile_ves]
                profy=[b[1] for a,b in self.profile_ves]
                self.plot.plot(x=profx, y=profy,size=20, pen=pg.mkPen('g'))
                self.listitem[-1].setText('Profile: '+'-'.join([p for p,q in self.profile_ves]))
            if event.double():
                # print('Double clicked...............')
                self.profiles.append(self.profile_ves)
                save_pkl(self.base_folder+'profiles.pkl',self.profiles)
                self.profile_ves=[]
                self.profiletobeselected=False
    


    def about(self):
        QMessageBox.about(self, "About Image Viewer",
            "<p>The <b>Image Viewer</b> example shows how to combine "
                        "(QScrollArea.widgetResizable), can be used to implement "
            "zooming and scaling features.</p>"
            "<p>In addition the example shows how to use QPainter to "
            "print an image.</p>")
    def makeProfile(self):
        self.profile_ves=[]
        for profile in self.profiles:
            if len(profile)>1:
                    profx=[b[0] for a,b in profile]
                    profy=[b[1] for a,b in profile]
                    self.plot.plot(x=profx, y=profy,size=20, pen=pg.mkPen('g'))
        self.profiletobeselected=True
    def createActions(self):
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)
        self.aboutAct = QAction("&About", self, triggered=self.about)
        self.makeProfileAct=QAction("&Make Profile",self,triggered=self.makeProfile)
    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.workMenu = QMenu("&Work", self)
        self.workMenu.addAction(self.makeProfileAct)
        # self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        # self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.workMenu)
        # self.menuBar().addMenu(self.digitizeMenu)
        self.menuBar().addMenu(self.helpMenu)

if __name__ == '__main__':
    
    import sys

    app = QApplication(sys.argv)
    imageViewer = ImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())
