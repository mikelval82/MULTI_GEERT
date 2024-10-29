# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""
from multiprocessing import Process

from FILTERS.filter_bank_manager import filter_bank_class
from FILTERS.spectrum import spectrum 

import numpy as np
#from datetime import datetime
#import time

class EEG_data_processing(Process):
    
    def __init__(self,
                 event,
                 buffer,
                 spectrogram_channel,
                 Spectrogram_radioButton_isChecked,
                 srate,
                 num_channels,
                 order,
                 lowcut,
                 highcut,
                 filtering_method):
        Process.__init__(self)
        self.event = event
        self.spectrogram_channel = spectrogram_channel
        self.Spectrogram_radioButton_isChecked = Spectrogram_radioButton_isChecked
        self.buffer = buffer
        self.filter_bank = filter_bank_class(srate, order, lowcut, highcut)
        self.spectrum = spectrum(SAMPLE_RATE=srate, CHANNELS=num_channels)
        self.filtering_method = filtering_method  # Now it's a shared value

    #        self.old = datetime.now().timestamp() * 1000
 
    def run(self):  
        while self.event.wait():
            
#            time.sleep(1)
            #################### DEFAULT FILTERING PROCESS ####################
            sample = self.buffer.get()
            if self.filtering_method.value == 'Butterworth':
                filtered = self.default_filtering( sample )
            else:
                filtered = np.asarray(sample)

            self.buffer.set_filtered(filtered)
            ###################################################################
            
            #*************** Compute Frequency Properties *********************
            if self.Spectrogram_radioButton_isChecked.value:
                data = self.spectrum.get_spectrogram( filtered[self.spectrogram_channel.value,:]).T
            else:
                data = self.spectrum.get_spectrum(filtered)

            self.buffer.set_spectral(data)
            #******************************************************************
#            new = datetime.now().timestamp() * 1000
#            print(self.name, ' processing: ', new-self.old)
#            self.old = new
            
    def default_filtering(self, data):
        self.filter_bank.update_filters()
        return self.filter_bank.pre_process( data )
                


        

  
    


        
                
    