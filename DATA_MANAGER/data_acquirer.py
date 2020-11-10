# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 
"""
from multiprocessing import Process, Value
from multiprocessing.managers import BaseManager
from DATA_MANAGER.data_manager import data_manager
import numpy as np
from datetime import datetime

class data_acquirer(Process):
    
    class MyManager(BaseManager):
        pass
     
    def Manager(self):
        m = self.MyManager()
        m.start()
        return m
    
    def __init__(self, inlets):
        Process.__init__(self)
        self.inlets = inlets     
        self.buffers = {'inlet':[], 'buffer':[], 'counter':[], 'recording':[]}
        self.old = datetime.now().timestamp() * 1000
        
    def set_up(self, num_channels, win_size, srate):
        for inlet in self.inlets:
            self.MyManager.register('buffer', data_manager)
            manager = self.Manager()
            self.buffers['inlet'].append( inlet )
            self.buffers['buffer'].append ( manager.buffer(num_channels,win_size,srate) )
            self.buffers['counter'].append( Value('i',0) )
            self.buffers['recording'].append( Value('i',0) )
            
    def run(self):     
        while True:
            for index in range(len(self.inlets)):
                sample, timestamp = self.buffers['inlet'][index].pull_sample(timeout=0.0)
                values = [is_recording.value for is_recording in self.buffers['recording']]
                if sample and np.any(values):
                    self.buffers['buffer'][index].append(sample, timestamp)   
                    self.buffers['counter'][index].value += 1
                    
                    new = datetime.now().timestamp() * 1000
                    print(' acquire: ', new-self.old, timestamp*1000)
                    self.old = new

        
                
    