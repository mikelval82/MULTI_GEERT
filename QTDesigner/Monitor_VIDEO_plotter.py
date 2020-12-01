# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 
"""
import pyqtgraph as pg
from PyQt5.QtCore import QRectF

class Monitor_VIDEO_plotter(pg.GraphicsWindow):
    pg.setConfigOption('background', 'k')
    pg.setConfigOption('foreground', 'm')
    
    def __init__(self, parent=None, **kargs):
        pg.GraphicsWindow.__init__(self, **kargs)
        self.setParent(parent)
        self.height = 480
        self.width = 640
    
    def create_plot(self):
        self.setWindowTitle('WEBCAM')
        self.show()
        self.view = self.addViewBox() 
        self.view.setAspectLocked(True) 
        self.img = pg.ImageItem(border='w') 
        self.view.addItem(self.img) 
        self.view.setRange(QRectF(0, 0, self.width, self.height))
        
    def update(self, sample):
        self.img.setImage( sample ) 
        
        
#%%
