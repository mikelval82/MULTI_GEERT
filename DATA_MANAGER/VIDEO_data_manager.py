# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""
import numpy as np
import cv2

class VIDEO_data_manager(object):
    
    def __init__(self):
        # --- constants -----
        self.initial_height = 240
        self.initial_width = 320
        self.height = 480
        self.width = 640
        self.win_size = 10
        self.data_shape = (self.width, self.height, 3, self.win_size)
        self.frame_shape = (self.width, self.height, 3)
        #--- data containers ---
        self.data = np.zeros(self.data_shape)
        self.stream_data = {'samples':[], 'timestamps':[]}
        #----- control params ----
        self.cur = 0
                 
    def reset(self):
        self.data = np.zeros(self.data_shape)
        self.stream_data = {'samples':[], 'timestamps':[]}
        self.cur = 0
        
    def append(self, sample, timestamp):
        """append an element at the end of the buffer"""  
        sample = np.reshape(np.array(sample), (self.initial_width, self.initial_height, 3))
        sample = cv2.resize(sample, (self.height,self.width), interpolation=cv2.INTER_AREA)
        self.data[:,:,:,self.cur % self.win_size] = np.array(sample)
        self.stream_data['samples'].append(sample)
        self.stream_data['timestamps'].append(timestamp)
        self.cur+=1 
            
    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        return self.data[:,:,:,self.cur % self.win_size - 1]
     
    def get_frame(self, index):
        """ Return a list of elements from the oldest to the newest. """
        return self.data[:,:,:,index]
    
    def get_stream(self, index=-1):
        if index == -1:
            return np.asarray(self.stream_data['samples'])
        else:
            return np.asarray(self.stream_data['samples'][index])
        
    def set_stream_label(self, sample):
        self.data[:,:,:,self.cur % self.win_size] = sample
        self.stream_data['samples'][-1] = sample
        self.stream_data['timestamps'][-1] = None
        self.cur+=1
        
    def set_filtered(self,x):
        self.filtered = x
        
    def get_filtered(self):
        return self.filtered
    
    def get_current_instant(self):
        return self.cur
        
    
    
    
    
    
    
