# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 10.5281/zenodo.3759306 
"""
#%%
from scipy.signal import butter, iirnotch, filtfilt
import numpy as np

class filter_bank_class: 
    def __init__(self, srate, order, lowcut, highcut):
        #---- constants -----
        self.LOWCUT = lowcut
        self.HIGHCUT = highcut
        self.ORDER = order
        self.SAMPLE_RATE = srate
        self.NOTCH = 50
         
    def update_filters(self):
        self.b0, self.a0 = self.notch_filter()
        self.b, self.a = self.butter_bandpass()

    def pre_process(self, sample):
        sample = np.array(sample)
        [fil,col] = sample.shape	
        sample_processed = np.zeros([fil,col])
        for i in range(fil):
            data = sample[i,:] 
            data = data - np.mean(data) 	
            if self.LOWCUT.value != None and self.HIGHCUT.value != None: # 
                data = self.butter_bandpass_filter(data)
            data = data + (i+1)*100 ### CUIDADO HARDCODING!!!!
            sample_processed[i,:] = data
  
        return sample_processed
        
    def notch_filter(self): # f0 50Hz, 60 Hz
        Q = 30.0  # Quality factor
        b0, a0 = iirnotch(self.NOTCH, Q, self.SAMPLE_RATE)#
        return b0,a0
    
    def butter_bandpass(self):
        nyq = int(0.5 * self.SAMPLE_RATE)
        low = self.LOWCUT.value / nyq
        high = self.HIGHCUT.value / nyq
        b, a = butter(self.ORDER.value, [low, high], btype='band')
        return b, a
    
    def butter_bandpass_filter(self, data):
        noth_data = filtfilt(self.b0, self.a0, data)
        band_passed_data = filtfilt(self.b, self.a, noth_data)
        return band_passed_data

    def butter_bandpass_specific_filter(self, data, lowcut, highcut, Fs, order):
        # -- notch filter --
        noth_data = filtfilt(self.b0, self.a0, data)
        # -- butterworth filter --
        nyq = 0.5 * Fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order , [low, high], btype='band')
        band_passed_data = filtfilt(b, a, noth_data)
        return band_passed_data
    
    def filter_bank(self, signal, Fs, filter_ranges, order=5):
        filterbank = []
        for [lowcut,highcut] in filter_ranges:
            y = self.butter_bandpass_specific_filter(signal, lowcut, highcut, Fs, order)
            filterbank.append(y)
        return np.asarray(filterbank)
    

        
    


