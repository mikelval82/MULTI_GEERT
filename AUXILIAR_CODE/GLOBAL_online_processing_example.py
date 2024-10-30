from PyQt5 import QtCore, QtWidgets  # Asegúrate de que QtWidgets está importado
from FILTERS.filter_bank_manager import FilterBank
from multiprocessing import Value
import pyqtgraph as pg
import numpy as np
import time


class simple_plot:
    pg.setConfigOption('background', 'k')
    pg.setConfigOption('foreground', 'm')

    def __init__(self, num_channels, scale, spacing):
        self.num_channels = num_channels
        self.scale = scale
        self.spacing = spacing
        self.win = pg.GraphicsLayoutWidget()  # Cambiado a GraphicsLayoutWidget
        self.win.resize(1000, 600)
        self.win.setWindowTitle('pyqtgraph example: Plotting')
        pg.setConfigOptions(antialias=True)

        self.plotter = self.win.addPlot(title="Updating plot")  # Aquí se añade el título correctamente
        self.curves = []
        for i in range(self.num_channels):
            self.curves.append(self.plotter.plot([], pen=(i, self.num_channels * 1.3)))

        self.win.show()  # Aseguramos que la ventana gráfica se muestre

    def normalize(self, sample):
        return (sample - np.mean(sample)) / np.std(sample)

    def update(self, sample):
        for i in range(self.num_channels):
            self.curves[i].setData(self.normalize(sample)[i] * self.scale + i * self.spacing)


class MyClass(QtCore.QThread):

    def __init__(self, current_GUI):
        super(MyClass, self).__init__(None)
        self.current_GUI = current_GUI
        # --- filter example --
        self.filter_bank = FilterBank(250, Value('i', 5), Value('i', 5), Value('i', 10))
        self.filter_bank.update_filters()
        # --- visualize ---
        self.plotters = []
        for _ in range(len(self.current_GUI.monitors)):
            self.plotters.append(simple_plot(8, 10, 2))

    def run(self):
        while True:
            time.sleep(.01)
            streamings = [monitor.streaming.value for monitor in self.current_GUI.monitors]

            if np.all(streamings):
                for index, monitor in enumerate(self.current_GUI.monitors):
                    sample = monitor.buffer.get()
                    filtered = self.myfilter(sample)
                    self.plotters[index].update(filtered)

    def myfilter(self, sample):
        return self.filter_bank.pre_process(sample)