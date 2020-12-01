# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""
import numpy as np

class EEG_data_manager(object):
    
    def __init__(self, num_channels=8, win_size=1500, srate=250):
        # --- constants -----
        self.num_channels = num_channels
        self.srate = srate
        self.win_size = win_size
        #--- data containers ---
        self.data = np.zeros((self.num_channels,self.win_size))
        self.filtered = np.zeros((self.num_channels,self.win_size))
        self.spectral = None
        self.stream_data = {'samples':[], 'timestamps':[]}
        #----- control params ----
        self.cur = 0
        self.recording = False
        
    def set_recording(self, recording):
        self.recording = recording
                 
    def reset(self, win_size):
        self.win_size = win_size
        self.data = np.zeros((self.num_channels,self.win_size))
        self.filtered = np.zeros((self.num_channels,self.win_size))
        self.stream_data = {'samples':[], 'timestamps':[]}
        self.cur = 0
        
    def append(self, sample, timestamp):
        """append an element at the end of the buffer"""  
        self.cur = self.cur % self.win_size
        self.data[:,self.cur] = np.asarray(sample).transpose()
        self.cur = self.cur+1  
        if self.recording:
            self.stream_data['samples'].append(np.asarray(sample).transpose())
            self.stream_data['timestamps'].append(timestamp)
            
    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        return list(self.data)
    
    def get_stream(self):
        return np.asarray(self.stream_data['samples'])
        
    def set_filtered(self,x):
        self.filtered = x
        
    def get_filtered(self):
        return self.filtered
        
    def set_spectral(self,x):
        self.spectral = x
        
    def get_spectral(self):
        return self.spectral
    
    def get_current_instant(self):
        return self.cur
        
    
    
    
    
    
    
