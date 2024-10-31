# -*- coding: utf-8 -*-
"""
@author: Mikel Val Calvo
@email: mvalcal1@upv.edu.es
@institution: Instituto Universitario de Investigación en Tecnología Centrada en el Ser Humano,
              Universitat Politècnica de València, València, Spain
"""

import numpy as np
from neurodsp import spectral
from lspopt.lsp import spectrogram_lspopt


class Spectrum:
    def __init__(self, sample_rate=250, channels=8):
        self.sample_rate = sample_rate
        self.channels = channels

    def get_spectrum(self, samples):
        """
        Compute the spectrum for each channel.

        Args:
            samples (np.ndarray): 2D array where each row represents a channel's time-series data.

        Returns:
            freqs (np.ndarray): Frequency values.
            spectrums (np.ndarray): Computed spectrum for each channel.
        """
        # Ensure input is a numpy array
        samples = np.asarray(samples)

        # Perform a single spectrum computation to determine the spectrogram shape
        freqs, initial_spectre = spectral.compute_spectrum(samples[0, :], self.sample_rate)
        spectrums = np.zeros((self.channels, len(initial_spectre)))

        # Calculate the spectrum for each channel
        for i in range(self.channels):
            _, spectre = spectral.compute_spectrum(samples[i, :], self.sample_rate)
            if spectre.shape[0] == spectrums.shape[1]:  # Ensure shapes match
                spectrums[i, :] = spectre
            else:
                spectrums = np.vstack([spectrums[:i], spectre, spectrums[i + 1:]])  # Adjust array shape if needed

        return freqs, spectrums

    def get_spectrogram(self, samples):
        """
        Compute the spectrogram for each channel.

        Args:
            samples (np.ndarray): 1D or 2D array of time-series data.

        Returns:
            Sxx (np.ndarray): Computed spectrogram for the sample.
        """
        # Ensure input is a numpy array
        samples = np.asarray(samples)

        # Use spectrogram_lspopt for optimal time-frequency resolution
        _, _, Sxx = spectrogram_lspopt(samples, self.sample_rate, c_parameter=20.0)

        return Sxx








