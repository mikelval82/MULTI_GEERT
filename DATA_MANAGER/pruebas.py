# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 
"""
from multiprocessing import Process
from multiprocessing.managers import BaseManager
import numpy as np
from pylsl import StreamInlet, resolve_stream
from FILTERS.filter_bank_manager import filter_bank_class
from FILTERS.spectrum import spectrum 
from datetime import datetime
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import time

class MyManager(BaseManager):
    pass
 
def Manager2():
    m = MyManager()
    m.start()
    return m
 
class RingBuffer(object):
    """ class that implements a not-yet-full buffer """
    
    def __init__(self, channels, length):
        self.channels = channels
        self.max = length 
        self.data = np.zeros((self.channels,self.max))
        self.cur = 0
        self.stream_data = []
        self.recording = False
        self.filtered = None
        
    def update(self, length):
        self.max = length
        self.data = np.zeros((self.channels,self.max))
        self.cur = self.max
         
    def reset(self):
        self.data = np.zeros((self.channels,self.max))
        self.cur = 0
        self.stream_data = []
        
    def append(self,x):
        """append an element at the end of the buffer"""  
        self.cur = self.cur % self.max
        self.data[:,self.cur] = np.asarray(x).transpose()
        self.cur = self.cur+1  
        if self.recording:
            self.stream_data.append(np.asarray(x).transpose())
            
    def set_filtered(self, x):
        self.filtered = x
        
    def get_filtered(self):
        return self.filtered
            
    def set_recording(self, recording):
        self.recording = recording
        
    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        return list(self.data)
    
    def get_stream_data(self):
        return self.stream_data

class acquire(Process):
    def __init__(self, inlet, buffer, name):
        Process.__init__(self)
        self.inlet = inlet
        self.buffer = buffer
        self.name = name
        self.old = datetime.now().timestamp() * 1000
        
    def run(self):
        while True:
            self.buffer.append(self.inlet.pull_sample()[0])
            new = datetime.now().timestamp() * 1000
            print(self.name, ' acquire: ', new-self.old)
            self.old = new
            
class processing(Process):
    def __init__(self, buffer, name):
        Process.__init__(self)
        self.buffer = buffer
        self.name = name
        self.filter_bank = filter_bank_class()
        self.filter_bank.update_filters()
        self.spectrum = spectrum(SAMPLE_RATE=250, CHANNELS=8)
        self.old = datetime.now().timestamp() * 1000
        
    def run(self):
        while True:
            filtered = self.filter_bank.pre_process( self.buffer.get() )
            self.buffer.set_filtered(filtered)
            self.spectrum.get_spectrum(filtered)
            new = datetime.now().timestamp() * 1000
            print(self.name, ' processing: ', new-self.old)
            self.old = new
        

                      
if __name__ == '__main__':
    MyManager.register('buffer', RingBuffer)
    
    streams = resolve_stream('type', 'EEG')
    inlet = StreamInlet(streams[0])
    
    manager = Manager2()
    buff = manager.buffer(8, 6*250)
    
    ack1 = acquire(inlet, buff, 'ack 1')
    ack1.start()
    pro1 = processing(buff, 'pro 1')
    pro1.start()
    
    window = pg.GraphicsWindow()
    plotter = window.addPlot()
    plotter.setLabel('left', 'Voltage', units='mV')
    plotter.setLabel('bottom', "Time", units='seg')
    plotter.showGrid(True, True, alpha = 0.5)
    plotter.setYRange(0, (8+1)*100)
    plotter.setXRange(0, 6*250)
    plotter.getAxis('left').setTicks([ [(100, 'FP1'), (200, 'FP2'), (300, 'C1'), (400, 'C2'), (500, 'P1'), (600, 'P2'), (700, 'O1'), (800, 'O2')] ])
    curves = []
    for i in range(8):
        curves.append( plotter.plot([], pen=(i,8*1.3)) )
        
    def update():
        global curves, buff
        for i in range(8):
            curves[i].setData(buff.get_filtered()[i])
        print('update')
            
    time.sleep(.1)
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(50)

    
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        

#            

        


    
    
    
    
