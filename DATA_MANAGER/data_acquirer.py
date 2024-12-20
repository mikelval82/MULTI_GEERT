# -*- coding: utf-8 -*-
"""
@author: Mikel Val Calvo
@email: mvalcal1@upv.edu.es
@institution: Instituto Universitario de Investigación en Tecnología Centrada en el Ser Humano,
              Universitat Politècnica de València, València, Spain
"""

from multiprocessing import Process, Value
from multiprocessing.managers import BaseManager
from DATA_MANAGER.EEG_data_manager import EEG_data_manager
import numpy as np
#import time
#from datetime import datetime

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
        self.buffers = {'inlet':[], 'buffer':[], 'counter':[], 'streaming':[], 'active':[]}
#        self.old = datetime.now().timestamp() * 1000
        
    def call_method(self, o, name, inlet, type):
        if type =='EEG':
            return getattr(o, name)(num_channels=inlet.channel_count, srate=inlet.info().nominal_srate())
        
    def set_up(self):
        for index, inlet in enumerate(self.inlets):
            if inlet.info().type() == 'EEG':
                self.MyManager.register('buffer_'+str(index), EEG_data_manager)
            # ---- set buffers -----
            self.buffers['inlet'].append( inlet ) 
            self.buffers['buffer'].append ( self.call_method(self.Manager(), 'buffer_'+str(index), inlet, inlet.info().type()) )
            self.buffers['counter'].append( Value('i',0) )
            self.buffers['streaming'].append( Value('i',0) )
            self.buffers['active'].append( Value('i',1) )
   
    def run(self): 
        while True:
#            time.sleep(1)            
            if not np.any([is_active.value for is_active in self.buffers['active']]):
                break
            else:
                for index in range(len(self.inlets)):
                    sample, timestamp = self.buffers['inlet'][index].pull_sample(timeout=0.0)  
#                    monitors_streaming = [is_streaming.value for is_streaming in self.buffers['streaming']]
                    if sample and self.buffers['streaming'][index].value:
                        self.buffers['buffer'][index].append(sample, timestamp)   
                        self.buffers['counter'][index].value += 1
                    
#                        new = datetime.now().timestamp() * 1000
#                        print(' acquire: ', new-self.old)
#                        self.old = new
#                    
        


















       
    