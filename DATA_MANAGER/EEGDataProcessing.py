# -*- coding: utf-8 -*-
"""
@author: Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos
@email: mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com
@institution: Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED);
              Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain;
              Neuroengineering medical group (UMH)
"""

from multiprocessing import Process
from FILTERS.filter_bank_manager import filter_bank_class
from FILTERS.spectrum import Spectrum
import numpy as np


class EEGDataProcessing(Process):

    def __init__(self,
                 event,
                 buffer,
                 spectrogram_channel,
                 spectrogram_checked,
                 srate,
                 num_channels,
                 order,
                 lowcut,
                 highcut,
                 filtering_method):
        super().__init__()
        self.event = event
        self.spectrogram_channel = spectrogram_channel
        self.spectrogram_checked = spectrogram_checked
        self.buffer = buffer
        self.filter_bank = filter_bank_class(srate, order, lowcut, highcut)
        self.spectrum = Spectrum(sample_rate=srate, channels=num_channels)
        self.filtering_method = filtering_method

    def run(self):
        while self.event.wait():
            sample = self.buffer.get()  # Get data from buffer

            # Apply filtering if the method is Butterworth
            if self.filtering_method.value == 'Butterworth':
                sample = self.default_filtering(sample)

            self.buffer.set_filtered(sample)  # Update buffer with filtered data

            # Calculate spectral properties based on spectrogram setting
            spectral_data = (self.spectrum.get_spectrogram(sample[self.spectrogram_channel.value, :]).T
                             if self.spectrogram_checked.value else
                             self.spectrum.get_spectrum(sample))

            self.buffer.set_spectral(spectral_data)  # Update buffer with spectral data

    def default_filtering(self, data):
        """
        Apply the default filtering method using the filter bank.

        Args:
            data (np.ndarray): Input EEG data to be filtered.

        Returns:
            np.ndarray: Filtered EEG data.
        """
        return self.filter_bank.pre_process(data)
