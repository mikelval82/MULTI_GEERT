# -*- coding: utf-8 -*-
"""
@author: Mikel Val Calvo
@email: mvalcal1@upv.edu.es
@institution: Instituto Universitario de Investigación en Tecnología Centrada en el Ser Humano,
              Universitat Politècnica de València, València, Spain
"""

import pyqtgraph as pg
from PyQt5.QtCore import QRectF

class Monitor_CARROUSEL_plotter(pg.GraphicsWindow):
    pg.setConfigOption('background', 'k')
    pg.setConfigOption('foreground', 'm')
    
    def __init__(self, parent=None, **kargs):
        pg.GraphicsWindow.__init__(self, **kargs)
        self.setParent(parent)
        self.height = 480
        self.width = 640
    
    def create_plot(self):
        self.show()
        self.view = self.addViewBox() 
        self.view.setAspectLocked(True) 
        self.img = pg.ImageItem(border='w') 
        self.view.addItem(self.img) 
        self.view.setRange(QRectF(0, 0, self.width, self.height ))
        
    def update(self, sample):
        self.img.setImage( sample ) 
