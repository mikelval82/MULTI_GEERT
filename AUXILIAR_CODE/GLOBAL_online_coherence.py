from PyQt5 import QtCore, QtWidgets
from FILTERS.filter_bank_manager import FilterBank
from multiprocessing import Value
import pyqtgraph as pg
import numpy as np
import time
from scipy.signal import coherence


class simple_plot:
    pg.setConfigOption('background', 'k')
    pg.setConfigOption('foreground', 'm')

    def __init__(self, num_channels, scale, spacing, num_pairs):
        self.num_channels = num_channels
        self.scale = scale
        self.spacing = spacing
        self.win = pg.GraphicsLayoutWidget()  # Cambiado a GraphicsLayoutWidget
        self.win.resize(1000, 600)
        self.win.setWindowTitle('Coherence Plot')
        pg.setConfigOptions(antialias=True)

        self.plotter = self.win.addPlot(title="Coherence Plot")
        self.curves = []

        # Create curves for each coherence pair
        for i in range(num_pairs):
            self.curves.append(self.plotter.plot([], pen=(i, num_pairs * 1.3)))

        self.win.show()  # Aseguramos que la ventana gráfica se muestre

    def update(self, coherence_values):
        # Update the plot with coherence values for each pair
        for i in range(len(self.curves)):
            self.curves[i].setData(coherence_values[i])


class MyClass(QtCore.QThread):

    def __init__(self, current_GUI):
        super(MyClass, self).__init__(None)
        self.current_GUI = current_GUI
        # --- filter example --
        self.filter_bank = FilterBank(250, Value('i', 5), Value('i', 5), Value('i', 10))

        # --- visualize coherence ---
        num_pairs = 8  # One pair for each channel (e.g., channel 0 of monitor 1 with channel 0 of monitor 2)
        self.plotter = simple_plot(8, 10, 2, num_pairs)  # Create only one plot instance for cross-monitor coherence

        # Parameters for coherence calculation
        self.coherence_freq = 250  # Sampling frequency of the EEG signal
        self.coherence_window = 256  # Window length for coherence calculation

    def run(self):
        while True:
            streamings = [monitor.streaming.value for monitor in self.current_GUI.monitors]

            if len(self.current_GUI.monitors) >= 2 and np.all(streamings):
                # Get the samples from both monitors
                sample_1 = self.current_GUI.monitors[0].buffer.get()
                sample_2 = self.current_GUI.monitors[1].buffer.get()

                # Filter the samples
                filtered_1 = self.myfilter(sample_1)
                filtered_2 = self.myfilter(sample_2)

                # Coherence calculation between monitors
                coherence_values = self.compute_coherence(filtered_1, filtered_2)

                # Update the plot with coherence values
                self.plotter.update(coherence_values)

    def myfilter(self, sample):
        return self.filter_bank.pre_process(sample)

    def compute_coherence(self, sample_1, sample_2):
        coherence_values = []

        # Iterate over each channel to compare the same channel from monitor 1 and monitor 2
        for ch in range(len(sample_1)):
            # Extract the data for the corresponding channels from both monitors
            signal_1 = sample_1[ch]
            signal_2 = sample_2[ch]

            # Compute coherence between the corresponding channels of the two monitors
            f, Cxy = coherence(signal_1, signal_2, fs=self.coherence_freq, nperseg=self.coherence_window)

            # Store coherence values for plotting
            coherence_values.append(Cxy)

        return coherence_values
