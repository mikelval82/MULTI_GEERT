# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 
"""
from multiprocessing import Process

from FILTERS.filter_bank_manager import filter_bank_class
from FILTERS.spectrum import spectrum 

from datetime import datetime

class data_processing(Process):
    
    def __init__(self, event, buffer, spectrogram_channel, Spectrogram_radioButton_isChecked, srate, num_channels, order, lowcut, highcut):
        Process.__init__(self)
        self.event = event
        self.spectrogram_channel = spectrogram_channel
        self.Spectrogram_radioButton_isChecked = Spectrogram_radioButton_isChecked
        self.buffer = buffer
        self.filter_bank = filter_bank_class(srate, order, lowcut, highcut)
        self.filter_bank.update_filters()
        self.spectrum = spectrum(SAMPLE_RATE=srate, CHANNELS=num_channels)
        self.old = datetime.now().timestamp() * 1000
        
    def run(self):  
        while self.event.wait():
            #------------ DEFAULT FILTERING PROCESS -------------------------------
            self.filter_bank.update_filters()
            filtered = self.filter_bank.pre_process( self.buffer.get() )
            self.buffer.set_filtered(filtered)
            #------------ Compute Frequency Properties ---------------------
            if self.Spectrogram_radioButton_isChecked.value:
                data = self.spectrum.get_spectrogram( filtered[self.spectrogram_channel.value,:]).T #ojo esta hardcodeado el canal!!!!!!!!!
            else:
                data = self.spectrum.get_spectrum(filtered)
            self.buffer.set_spectral(data)
            
            new = datetime.now().timestamp() * 1000
            print(self.name, ' processing: ', new-self.old)
            self.old = new
                
                    
            
                

    
  
    


        
                
    