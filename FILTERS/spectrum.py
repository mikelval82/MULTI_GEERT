# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""
#%%
import numpy as np
#from scipy import signal
from neurodsp import spectral
from lspopt.lsp import spectrogram_lspopt

class spectrum:
    def __init__(self, SAMPLE_RATE=250, CHANNELS=8):
        self.SAMPLE_RATE = SAMPLE_RATE
        self.CHANNELS = CHANNELS
        
    def get_spectrum(self, samples):
        spectrums = []
        for i in range(self.CHANNELS):
             freqs, spectre  = spectral.compute_spectrum(samples[i,:], self.SAMPLE_RATE)
             spectrums.append(spectre)
        return freqs, np.asarray(spectrums)
    
    def get_spectrogram(self, samples):
#        _, _, Sxx = signal.spectrogram(samples, self.constants.SAMPLE_RATE)
        _,_, Sxx = spectrogram_lspopt(samples, self.SAMPLE_RATE, c_parameter=20.0)
        return Sxx
        
