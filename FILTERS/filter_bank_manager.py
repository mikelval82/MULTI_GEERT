import numpy as np
from scipy.signal import butter, iirnotch, filtfilt


class filter_bank_class:
    def __init__(self, srate, order, lowcut, highcut):
        self.LOWCUT = lowcut
        self.HIGHCUT = highcut
        self.ORDER = order
        self.SAMPLE_RATE = srate
        self.NOTCH = 50
        self._initialize_filters()

    def _initialize_filters(self):
        self.b0, self.a0 = self.notch_filter()
        self.b, self.a = self.butter_bandpass()

    def pre_process(self, sample):
        sample = np.array(sample)
        sample -= np.mean(sample, axis=1, keepdims=True)  # Vectorized mean subtraction
        if self.LOWCUT.value is not None and self.HIGHCUT.value is not None:
            sample = self.butter_bandpass_filter(sample)
        return sample

    def notch_filter(self):
        Q = 30.0
        return iirnotch(self.NOTCH, Q, self.SAMPLE_RATE)

    def butter_bandpass(self):
        nyq = 0.5 * self.SAMPLE_RATE
        low, high = self.LOWCUT.value / nyq, self.HIGHCUT.value / nyq
        return butter(self.ORDER.value, [low, high], btype='band')

    def butter_bandpass_filter(self, data):
        return filtfilt(self.b, self.a, filtfilt(self.b0, self.a0, data, axis=1), axis=1)
