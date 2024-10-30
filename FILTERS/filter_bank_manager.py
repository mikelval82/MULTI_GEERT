import numpy as np
from scipy.signal import butter, iirnotch, filtfilt


class FilterBank:
    def __init__(self, srate, order, lowcut, highcut):
        self.LOWCUT = lowcut  # This is a multiprocessing.Value
        self.HIGHCUT = highcut  # This is a multiprocessing.Value
        self.ORDER = order
        self.SAMPLE_RATE = srate
        self.NOTCH = 50
        self._initialize_filters()

    def _initialize_filters(self):
        self.b0, self.a0 = self.notch_filter()
        self.b, self.a = self.butter_bandpass()

    def update_cutoffs(self, lowcut, highcut):
        """
        Updates the lowcut and highcut values and reinitializes the filters.

        Args:
            lowcut (float): New lowcut frequency.
            highcut (float): New highcut frequency.
        """
        self.LOWCUT.value = lowcut
        self.HIGHCUT.value = highcut
        self._initialize_filters()  # Reinitialize filters with new cutoffs

    def pre_process(self, sample):
        sample = np.array(sample)
        sample -= np.mean(sample, axis=1, keepdims=True)
        if self.LOWCUT.value is not None and self.HIGHCUT.value is not None:
            sample = self.butter_bandpass_filter(sample)
        return sample

    def notch_filter(self):
        Q = 30.0
        return iirnotch(self.NOTCH, Q, self.SAMPLE_RATE)

    def butter_bandpass(self):
        nyq = 0.5 * self.SAMPLE_RATE
        low, high = self.LOWCUT.value / nyq, self.HIGHCUT.value / nyq  # Access .value here
        return butter(self.ORDER.value, [low, high], btype='band')

    def butter_bandpass_filter(self, data):
        return filtfilt(self.b, self.a, filtfilt(self.b0, self.a0, data, axis=1), axis=1)
