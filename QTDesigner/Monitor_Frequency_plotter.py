# -*- coding: utf-8 -*-
"""
@author: Mikel Val Calvo
@email: mvalcal1@upv.edu.es
@institution: Instituto Universitario de Investigación en Tecnología Centrada en el Ser Humano,
              Universitat Politècnica de València, València, Spain
"""

import pyqtgraph as pg
import numpy as np


class Monitor_Frequency_plotter(pg.GraphicsLayoutWidget):  # Cambiado de GraphicsWindow a GraphicsLayoutWidget
    pg.setConfigOption('background', 'k')
    pg.setConfigOption('foreground', 'm')

    def __init__(self, parent=None, **kargs):
        super().__init__(**kargs)  # Utiliza super() para inicializar correctamente la clase heredada
        self.setParent(parent)
        self.curves = []
        self.Spectrogram_radioButton_isChecked = False
                
    def set_params(self, num_channels=8):
        self.num_channels = num_channels
        
    def create_spectrogram_plot(self):
        self.setWindowTitle('Spectrogram')
        self.plotter = self.addPlot()
        self.plotter.setLabel('left', 'Frequency', units='Hz')
        self.plotter.setLabel('bottom', "Samples", units='n')
        self.plotter.showGrid(True, True, alpha = 0.5)
        self.plotter.setLogMode(False, False)
        
        self.spectrogram_Img = pg.ImageItem()     
        self.plotter.addItem(self.spectrogram_Img)

        pos = np.array([0.0, 0.5, 1.0])
        color = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
        map = pg.ColorMap(pos, color)
        lut = map.getLookupTable(0.0, 1.0, 256)           
        self.spectrogram_Img.setLookupTable(lut)
        
    def create_fft_plot(self):
        self.setWindowTitle('Spectrogram')
        self.plotter = self.addPlot()
        self.plotter.setLabel('left', 'Amplitude', units='dB')
        self.plotter.setLabel('bottom', "Frequency", units='Hz')
        self.plotter.showGrid(True, True, alpha = 0.5)
        self.plotter.setLogMode(False, True)

        for i in range(self.num_channels):
            c = pg.PlotCurveItem(pen=(i,self.num_channels*1.3))
            self.plotter.addItem(c)
            self.curves.append(c)
            
    def select_mode(self, radioButton):
        self.removeItem(self.plotter)
        if radioButton.isChecked():
            self.create_spectrogram_plot()
            self.Spectrogram_radioButton_isChecked = True
        else:
            self.curves = []
            self.create_fft_plot()    
            self.Spectrogram_radioButton_isChecked = False

    def update_spectrum(self, sample):
        try:
            if self.Spectrogram_radioButton_isChecked:
                self.spectrogram_Img.setImage(sample, autoLevels=True)
            else:
                for i in range(self.num_channels):
                    self.curves[i].setData(np.asarray(sample[0]),np.log10(np.asarray(sample[1])[i,:]))
        except Exception as e:
            print('Error in update_spectrum: ', e)
            print(sample)
            pass
