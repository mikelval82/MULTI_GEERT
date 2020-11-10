# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 
"""
from multiprocessing import Value, Event
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import xml.etree.ElementTree as ET

from QTDesigner.EEG_monitor import Ui_EEG_Viewer as UI
from DATA_MANAGER.data_processing import data_processing
from DYNAMIC.dynamic import dynamic
from DATA_MANAGER.file_IO import io_manager

class EEG_monitor_wrapper(QMainWindow, UI):
    
    def __init__(self, inlet_info, buffer, counter, recording):
        QMainWindow.__init__(self, parent=None)
        # --- buffer ----
        self.inlet_info = inlet_info
        self.buffer = buffer
        self.counter = counter
        #---- GUI setup ----------
        self.setupUi(self)
        self.setWindowTitle(self.inlet_info.name())
        self.show()
        #----- control params ----
        self.streaming = recording
        self.Spectrogram_radioButton_isChecked = Value('b',0)
        #--- global params -----
        self.name = self.inlet_info.name()
        self.refresh_rate = 50
        self.srate = int(self.inlet_info.nominal_srate())
        self.num_channels = 8#self.buffer_container['inlet'].channel_count
        self.win_size = int(self.srate * int(self.WindowsSize_LineEdit.text()))
        self.channels = []
        self.get_labels(ET.fromstring(self.inlet_info.as_xml()))
        #----- shared variables ------------
        self.order = Value('i',5)
        self.lowcut = Value('i',1)
        self.highcut = Value('i', 75)
        self.spectrogram_channel = Value('i',0)
        self.event = Event()
        #---- IO -----
        self.io = io_manager()
        #---- streaming processing ----
        self.processing = data_processing(self.event, self.buffer, self.spectrogram_channel, self.Spectrogram_radioButton_isChecked, self.srate, self.num_channels, self.order, self.lowcut, self.highcut)
        self.processing.start()
        #---- setup monitors ------
        self.EEG_monitor.set_params( self.channels, self.counter, num_channels=self.num_channels, x_dim=self.win_size, y_dim=(self.num_channels+1)*100)
        self.EEG_monitor.create_plot() 
        self.EEG_monitor.channels = self.channels
        self.Frequency_monitor.set_params(num_channels=self.num_channels)
        self.Frequency_monitor.create_fft_plot()
        #---- dynamic imports ------------
        self.dyn = dynamic(self, None, None)#el primer None hay que cambiarlo por el acceso a los streams!!!!!!
        #---- callbacks ------
        self.Filename_btn.clicked.connect(self.saveFileDialog)
        self.Import_btn.clicked.connect(self.openFileNameDialog)
        self.Start_btn.clicked.connect(lambda: self.run('SHOW'))
        self.Record_btn.clicked.connect(lambda: self.run('RECORD'))
        self.ButterOrder_LineEdit.textChanged.connect(lambda: self.update('FREQ', 'ORDER', self.ButterOrder_LineEdit.text() ))
        self.WindowsSize_LineEdit.textChanged.connect(lambda: self.update('TIME', 'LENGTH', self.WindowsSize_LineEdit.text() ))
        self.FrequencyRange_ComboBox.currentIndexChanged.connect(lambda: self.update('FREQ', 'BAND', self.FrequencyRange_ComboBox.currentText() ))
        self.FiletringMethod_ComboBox.currentIndexChanged.connect(lambda: self.update('FREQ', 'METHOD', self.FiletringMethod_ComboBox.currentText() ))
        self.Spectrogram_radioButton.toggled.connect(self.select_mode)
        self.Spectrogram_radioButton.toggled.connect(lambda: self.Frequency_monitor.select_mode(self.Spectrogram_radioButton))
        self.Channels_ComboBox.addItems(self.channels)
        self.Channels_ComboBox.currentIndexChanged.connect(lambda: self.update( 'FREQ', 'CHANNEL', self.Channels_ComboBox.currentIndex() ))
        self.AddMarker_btn.clicked.connect(lambda: self.add_marker(self.Markers_ComboBox.currentText()) )
        self.scale_Slider.valueChanged.connect(lambda: self.EEG_monitor.set_scale(self.scale_Slider.value()))
        self.space_Slider.valueChanged.connect(lambda: self.EEG_monitor.set_space(self.space_Slider.value()))
        self.verticalScrollBar.valueChanged.connect(lambda: self.EEG_monitor.set_scroll(self.verticalScrollBar.value()))
        #-----------------------------------------------------------------------------------------------------------
        self.shorcuts = self.define_global_shortcuts()
        #--- visualize timer ----
        self.timer = QtCore.QTimer()
        self.timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer.timeout.connect(self.visualize)
        
        self.actionQuit = QtWidgets.QAction("Quit", self)
        self.actionQuit.triggered.connect(QtWidgets.QApplication.quit)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)        

    def get_labels(self, elem):
        if elem.tag == 'label':
            self.channels.append(elem.text)
        for child in elem.findall('*'):
            self.get_labels(child)

    def closeEvent(self, event):
        self.processing.kill()
        self.close()
        print('close window')
        
    def update(self, which, param, value):
        if value != '':
            if which == 'FREQ':
                if param == 'BAND':
                    if param ==  'ORDER':
                        self.order.value = int(value)
                    elif value == 'All':
                        self.lowcut.value = 1
                        self.highcut.value = int(self.srate/2 - 1)
                    elif value == 'Delta':
                        self.lowcut.value = 1
                        self.highcut.value = 5
                    elif value == 'Theta':
                        self.lowcut.value = 5
                        self.highcut.value = 10
                    elif value == 'Alpha':
                        self.lowcut.value = 10
                        self.highcut.value = 15
                    elif value == 'Beta':
                        self.lowcut.value = 15
                        self.highcut.value = 30
                    elif value == 'Gamma':
                        self.lowcut.value = 30
                        self.highcut.value = int(self.srate/2 - 1)   
                elif param == 'CHANNEL':
                    self.spectrogram_channel.value = value
            elif which == 'TIME':
                if param == 'LENGTH':
                    self.length = int(value)
                elif param == 'SRATE':
                    self.srate = int(value)
                self.win_size = self.srate * self.length  
                self.buffer.reset(self.win_size)
                self.EEG_monitor.redraw( self.win_size )
       
    def define_global_shortcuts(self):
        shortcuts = []
        sequence = {
            'Ctrl+s': lambda:  self.run('SHOW'),
            'Ctrl+r': lambda:  self.run('RECORD'),
            'Alt+0': lambda:  self.add_marker('Label_0'),
            'Alt+1': lambda:  self.add_marker('Label_1'),
            'Alt+2': lambda:  self.add_marker('Label_2'),
            'Alt+3': lambda:  self.add_marker('Label_3'),
            'Alt+4': lambda:  self.add_marker('Label_4'),
            'Alt+5': lambda:  self.add_marker('Label_5'),
            'Alt+6': lambda:  self.add_marker('Label_6'),
            'Alt+7': lambda:  self.add_marker('Label_7'),
            'Alt+8': lambda:  self.add_marker('Label_8'),
            'Alt+9': lambda:  self.add_marker('Label_9'),
        }
        for key, value in list(sequence.items()):
            s = QShortcut(QKeySequence(key),self, value)
            shortcuts.append(s)
        return shortcuts
        
    def add_marker(self, mark):
        if self.io.ispath:
            self.io.online_annotation(mark, self.buffer.get_current_instant())
        self.EEG_monitor.draw_vertical_line(mark)

    def run(self, action):
        if action == 'SHOW' and not self.streaming.value:
            self.event.set()
            self.timer.start(self.refresh_rate)
        elif action == 'SHOW' and self.streaming.value:
            self.event.clear()
            self.timer.stop()
            self.buffer.reset(self.win_size)
        elif action == 'RECORD' and not self.streaming.value:
            self.event.set()
            self.buffer.set_recording(True)
            self.io.online_annotation(action, self.buffer.get_current_instant())
            self.timer.start(self.refresh_rate)
        elif action == 'RECORD' and self.streaming.value:
            self.event.clear()
            self.buffer.set_recording(False)
            self.timer.stop()
            self.buffer.reset(self.win_size)
            self.io.online_annotation(action, self.buffer.get_current_instant())
            self.io.append_to_file(self.buffer.get_stream())
            self.io.close_file()
        self.streaming.value = not self.streaming.value
     
    def visualize(self):
        self.EEG_monitor.update(self.buffer.get_filtered())
        self.Frequency_monitor.update(self.buffer.get_spectral())

    def select_mode(self):
        self.Spectrogram_radioButton_isChecked.value = self.Spectrogram_radioButton.isChecked()
        
    def saveFileDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","EDF Files (*.edf)", options=options)
        if fileName:
            self.io.create_file(fileName)
            
    def openFileNameDialog(self, btn):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileType = "PYTHON Files (*.py)"
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","",fileType, options=options)       
        #----------------- LOAD AND EXECUTE THE MODULE -----#
        self.dyn.load_module(fileName)
        

        
 

        

    