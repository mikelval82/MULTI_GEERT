# -*- coding: utf-8 -*-
"""
@author: Mikel Val Calvo
@email: mvalcal1@upv.edu.es
@institution: Instituto Universitario de Investigación en Tecnología Centrada en el Ser Humano,
              Universitat Politècnica de València, València, Spain
"""

import pyqtgraph as pg
from pyqtgraph import Point
import numpy as np


class Monitor_EEG_plotter(pg.GraphicsLayoutWidget):  # Cambiado de GraphicsWindow a GraphicsLayoutWidget
    pg.setConfigOption('background', 'k')
    pg.setConfigOption('foreground', 'm')

    def __init__(self, parent=None, **kargs):
        super().__init__(**kargs)  # Utiliza super() para heredar correctamente de GraphicsLayoutWidget
        self.setParent(parent)
    
    def set_params(self, channels, contador, num_channels=8, x_dim=250, y_dim=900):
        self.num_channels = num_channels
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.curves = []
        self.lines = {'lines':[], 'points':[], 'counter':[]}
        self.scale = 50
        self.positions = [(i+1)*100 for i in range(self.num_channels)]
        self.channels = channels
        self.contador = contador
        
    def set_scale(self, value):
        self.scale = value
        
    def set_space(self, value):
        self.positions = [(i+1)*100*(value/100+1)for i in range(self.num_channels)]
        
    def set_scroll(self, value):
        max0 = (self.num_channels+1)*100
        x = self.positions[-1] - (self.num_channels+1)*100
        desp = (value/100)*x
        self.plotter.setYRange(value + desp, max0 + desp + value)
        
    def redraw(self, value):
        self.x_dim = value
        self.plotter.setXRange(0, self.x_dim)

    def draw_vertical_line(self, label):
        item = pg.InfiniteLine(movable=True, angle=90, label=label, pen=pg.mkPen('y', width=3), 
                               labelOpts={'position':.9, 'color': (100,255,100), 'fill': (100,255,100,30), 'movable': True})
        self.plotter.addItem(item)
        self.lines['lines'].append( item )
        self.lines['points'].append( Point(0,0) )
        self.lines['counter'].append( self.contador.value )
     
    def create_plot(self):
        self.setWindowTitle('EEG')
        self.plotter = self.addPlot()
        self.plotter.setLabel('left', 'Voltage', units='mV')
        self.plotter.setLabel('bottom', "Time", units='seg')
        self.plotter.showGrid(True, True, alpha = 0.5)
        self.plotter.setYRange(0, (self.num_channels+1)*100)
        self.plotter.setXRange(0, self.x_dim)
        ###### !!!!!! aqui falta sacar del inlet del damanager los nombres de los canales, y calcular las posiciones de forma automatica segun el y_dim!!!!!!!!!!1
#        self.plotter.getAxis('left').setTicks([ [(100, 'FP1'), (200, 'FP2'), (300, 'C1'), (400, 'C2'), (500, 'P1'), (600, 'P2'), (700, 'O1'), (800, 'O2')] ])
        self.plotter.getAxis('left').setTicks([[(pos, channel) for pos,channel in zip(self.positions, self.channels) ]])
        for i in range(self.num_channels):
            self.curves.append( self.plotter.plot([], pen=(i,self.num_channels*1.3)) )
            
    def normalize(self, sample):
        try:
            return (sample-np.mean(sample))/np.std(sample)
        except:
            return sample
    
    def remove_lines(self):
        if self.lines['lines']:
            for line in self.lines['lines']:
                self.plotter.removeItem(line)
        
    def update(self, sample):
        sample = self.normalize(sample)
        self.plotter.getAxis('left').setTicks([[(pos, channel) for pos,channel in zip(self.positions, self.channels) ]])
        #-----  draw curves ---------------------------
        for i in range(self.num_channels):
            self.curves[i].setData(sample[i] * self.scale + self.positions[i])
        #--------- draw markers -----------------------
        if self.lines:
            for line, point, counter in zip(self.lines['lines'], self.lines['points'], self.lines['counter']):
                point[0] = self.contador.value-counter
                line.setPos(point)
                if point[0] >= self.x_dim:
                    self.plotter.removeItem(line)
        
