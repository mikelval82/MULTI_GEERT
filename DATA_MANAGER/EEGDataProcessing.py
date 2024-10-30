from FILTERS.filter_bank_manager import FilterBank
from FILTERS.spectrum import Spectrum
import numpy as np
from multiprocessing import Process

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
        self.filter_bank = FilterBank(srate, order, lowcut, highcut)
        self.spectrum = Spectrum(sample_rate=srate, channels=num_channels)
        self.filtering_method = filtering_method
        # Initialize to track changes
        self.last_lowcut = lowcut.value
        self.last_highcut = highcut.value
        self.lowcut = lowcut
        self.highcut = highcut

    def run(self):
        while self.event.wait():
            # Update filter parameters if needed
            self.update_filter_params()

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

    def update_filter_params(self):
        """Check for updates in lowcut and highcut and reinitialize filters if changed."""
        if self.lowcut.value != self.last_lowcut or self.highcut.value != self.last_highcut:
            self.filter_bank.update_cutoffs(self.lowcut.value, self.highcut.value)
            self.last_lowcut = self.lowcut.value
            self.last_highcut = self.highcut.value

    def default_filtering(self, data):
        """
        Apply the default filtering method using the filter bank.

        Args:
            data (np.ndarray): Input EEG data to be filtered.

        Returns:
            np.ndarray: Filtered EEG data.
        """
        return self.filter_bank.pre_process(data)
