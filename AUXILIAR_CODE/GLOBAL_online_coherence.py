from PyQt5 import QtCore, QtWidgets
from FILTERS.filter_bank_manager import filter_bank_class
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
        self.filter_bank = filter_bank_class(250, Value('i', 5), Value('i', 5), Value('i', 10))
        self.filter_bank.update_filters()

        # --- visualize coherence ---
        num_pairs = 2  # Example: coherence between two pairs of channels
        self.plotters = []
        for _ in range(len(self.current_GUI.monitors)):
            self.plotters.append(simple_plot(8, 10, 2, num_pairs))

        # Parameters for coherence calculation
        self.coherence_freq = 250  # Sampling frequency of the EEG signal
        self.coherence_window = 256  # Window length for coherence calculation
        self.channel_pairs = [(0, 1), (2, 3)]  # Example pairs of channels to compute coherence between

    def run(self):
        while True:
            time.sleep(.01)
            streamings = [monitor.streaming.value for monitor in self.current_GUI.monitors]

            if np.all(streamings):
                for index, monitor in enumerate(self.current_GUI.monitors):
                    sample = monitor.buffer.get()
                    filtered = self.myfilter(sample)

                    # Coherence calculation
                    coherence_values = self.compute_coherence(filtered)

                    # Update plot with coherence values
                    self.plotters[index].update(coherence_values)

    def myfilter(self, sample):
        return self.filter_bank.pre_process(sample)

    def compute_coherence(self, sample):
        coherence_values = []

        # Iterate over the defined channel pairs
        for ch1, ch2 in self.channel_pairs:
            # Extract the data for the two channels
            signal_1 = sample[ch1]
            signal_2 = sample[ch2]

            # Compute coherence between the two channels
            f, Cxy = coherence(signal_1, signal_2, fs=self.coherence_freq, nperseg=self.coherence_window)

            # Store coherence values for plotting
            coherence_values.append(Cxy)

        return coherence_values
