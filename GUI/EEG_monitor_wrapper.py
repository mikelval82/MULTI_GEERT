from multiprocessing import Value, Event, Manager
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import xml.etree.ElementTree as ET
import numpy as np

from QTDesigner.EEG_monitor import Ui_EEG_Viewer as UI
from DATA_MANAGER.EEGDataProcessing import EEGDataProcessing
from DYNAMIC.dynamic import dynamic
from DATA_MANAGER.file_IO import io_manager
from GUI.EEG_monitor_shortcuts_manager import EEG_shortcuts


class EEG_monitor_wrapper(QMainWindow, UI):
    # Define signals
    annotation_signal = QtCore.pyqtSignal(str, float, float)  # For annotations: (event, instant, duration)
    file_save_signal = QtCore.pyqtSignal(np.ndarray)  # For saving the file: the stream to be saved

    def __init__(self, log, inlet, buffer, counter, streaming, active):
        super(EEG_monitor_wrapper, self).__init__(parent=None)
        #---- GUI setup ----------
        self.setupUi(self)
        self.setWindowTitle(inlet.info().name())

        # --- buffer related data structures ----
        self.log = log
        self.inlet = inlet
        self.buffer = buffer
        self.counter = counter
        self.streaming = streaming
        self.recording = False
        self.active = active
        self.is_shown = True

        #--- global params -----
        self.name = self.inlet.info().name()
        self.srate = int(self.inlet.info().nominal_srate())
        self.num_channels = self.inlet.channel_count
        self.win_size = int(self.srate * int(self.WindowsSize_LineEdit.text()))
        self.channels = []
        self.get_labels(ET.fromstring(self.inlet.info().as_xml()))

        #----- shared variables ------------
        self.order = Value('i', 5)
        self.lowcut = Value('i', 1)
        self.highcut = Value('i', 75)
        self.spectrogram_channel = Value('i', 0)
        self.Spectrogram_radioButton_isChecked = Value('b', 0)
        self.event = Event()
        manager = Manager()
        self.filtering_method = manager.Value('c', 'None')  # Shared memory for filtering method

        #---- IO -----
        self.io = io_manager(self.name)

        # Setup signals
        self.annotation_signal.connect(self.handle_annotation)  # Connect signal to handle annotation
        self.file_save_signal.connect(self.handle_file_save)  # Connect signal to handle file save

        #---- streaming processing ----
        self.processing = EEGDataProcessing(
            self.event,
            self.buffer,
            self.spectrogram_channel,
            self.Spectrogram_radioButton_isChecked,
            self.srate,
            self.num_channels,
            self.order,
            self.lowcut,
            self.highcut,
            self.filtering_method
        )
        self.processing.start()

        #---- setup monitors ------
        self.EEG_monitor.set_params(self.channels, self.counter, num_channels=self.num_channels, x_dim=self.win_size, y_dim=(self.num_channels + 1) * 100)
        self.EEG_monitor.create_plot()
        self.Frequency_monitor.set_params(num_channels=self.num_channels)
        self.Frequency_monitor.create_fft_plot()

        #---- dynamic imports ------------
        self.dyn = dynamic(self, None, None)  # el primer None hay que cambiarlo por el acceso a los streams!!!!!!

        #---- callbacks ------
        self.Filename_btn.clicked.connect(self.saveFileDialog)
        self.Import_btn.clicked.connect(self.openFileNameDialog)
        self.Start_btn.clicked.connect(lambda: self.run('SHOW'))
        self.Record_btn.clicked.connect(lambda: self.run('RECORD'))

        self.ButterOrder_LineEdit.textChanged.connect(lambda: self.update('FREQ', 'ORDER', self.ButterOrder_LineEdit.text()))
        self.WindowsSize_LineEdit.textChanged.connect(lambda: self.update('TIME', 'LENGTH', self.WindowsSize_LineEdit.text()))
        self.FrequencyRange_ComboBox.currentIndexChanged.connect(lambda: self.update('FREQ', 'BAND', self.FrequencyRange_ComboBox.currentText()))
        self.FiletringMethod_ComboBox.currentIndexChanged.connect(lambda: self.update('FREQ', 'METHOD', self.FiletringMethod_ComboBox.currentText()))

        self.Spectrogram_radioButton.toggled.connect(self.select_mode)
        self.Spectrogram_radioButton.toggled.connect(lambda: self.Frequency_monitor.select_mode(self.Spectrogram_radioButton))

        self.Channels_ComboBox.addItems(self.channels)
        self.Channels_ComboBox.currentIndexChanged.connect(lambda: self.update('FREQ', 'CHANNEL', self.Channels_ComboBox.currentIndex()))

        self.AddMarker_btn.clicked.connect(lambda: self.add_marker(self.Markers_ComboBox.currentText()))
        self.scale_Slider.valueChanged.connect(lambda: self.EEG_monitor.set_scale(self.scale_Slider.value()))
        self.space_Slider.valueChanged.connect(lambda: self.EEG_monitor.set_space(self.space_Slider.value()))
        self.verticalScrollBar.valueChanged.connect(lambda: self.EEG_monitor.set_scroll(self.verticalScrollBar.value()))

        #--- visualize timer ----
        self.timer = QtCore.QTimer()
        self.timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer.timeout.connect(self.visualize)
        self.refresh_rate = 50

        #---- close the sub-app -------
        self.actionQuit = QtWidgets.QAction("Quit", self)
        self.actionQuit.triggered.connect(QtWidgets.QApplication.quit)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    def run(self, action):
        if not self.streaming.value and not self.recording and action == 'SHOW':
            self.streaming.value = True
            self.EEG_monitor.remove_lines()
            self.buffer.reset(self.win_size)
            self.event.set()
            self.timer.start(self.refresh_rate)

        elif not self.streaming.value and not self.recording and action == 'RECORD':
            self.streaming.value = True
            self.recording = True
            self.EEG_monitor.remove_lines()
            self.buffer.set_recording(True)
            self.buffer.reset(self.win_size)
            try:
                self.io.create_file()
                # Use signal to emit annotation
                self.annotation_signal.emit(action, self.buffer.get_current_instant(), -1)
                self.log.myprint_in(f'File created at device: {self.name} subject: {self.io.fileName} Trial: {self.io.Trial}')
            except:
                self.log.myprint_error(f'Cannot create subject data file at device: {self.name}')
            finally:
                self.event.set()
                self.timer.start(self.refresh_rate)

        elif self.streaming.value and not self.recording and action == 'SHOW':
            self.streaming.value = False
            self.event.clear()
            self.timer.stop()

        elif self.streaming.value and not self.recording and action == 'RECORD':
            self.recording = True
            self.buffer.reset(self.win_size)
            self.buffer.set_recording(True)
            try:
                self.io.create_file()
                self.annotation_signal.emit(action, self.buffer.get_current_instant(), -1)
                self.log.myprint_in(f'File created at device: {self.name} subject: {self.io.fileName} Trial: {self.io.Trial}')
            except:
                self.log.myprint_error(f'Cannot create subject data file at device: {self.name}')

        elif self.streaming.value and self.recording and action == 'RECORD':
            self.streaming.value = False
            self.recording = False
            self.buffer.set_recording(False)
            self.event.clear()
            self.timer.stop()
            try:
                current_instant = self.buffer.get_current_instant()
                self.annotation_signal.emit(action, current_instant, -1)
                self.file_save_signal.emit(self.buffer.get_stream())  # Use signal to emit stream to be saved
                self.log.myprint_out(f'File saved at device: {self.name} subject: {self.io.fileName} Trial: {self.io.Trial-1}')
            except:
                self.log.myprint_error(f'Cannot close subject data file at device: {self.name}')
            finally:
                self.buffer.reset(self.win_size)
                self.buffer.set_recording(False)

        elif self.streaming.value and action not in ['SHOW', 'RECORD']:
            self.add_marker(action)

    def handle_annotation(self, event, instant, duration):
        """Handle the annotation safely."""
        self.io.online_annotation(event, instant, duration)

    def handle_file_save(self, stream):
        """Handle file saving safely."""
        self.io.append_to_file(stream)
        self.io.close_file()

    def get_labels(self, elem):
        if elem.tag == 'label':
            self.channels.append(elem.text)
        for child in elem.findall('*'):
            self.get_labels(child)

    def closeEvent(self, event):
        self.active.value = False
        self.processing.kill()
        self.close()

    def update(self, which, param, value):
        print(f'update -> {which}, {param}, {value}')
        if value != '':
            if which == 'FREQ':
                if param == 'BAND':
                    if value == 'All':
                        self.lowcut.value = 1
                        self.highcut.value = int(self.srate / 2 - 1)
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
                        self.highcut.value = int(self.srate / 2 - 1)

                elif param == 'METHOD':
                    self.processing.filtering_method.value = value
                elif param == 'CHANNEL':
                    self.spectrogram_channel.value = value
            elif which == 'TIME':
                if param == 'LENGTH':
                    self.length = int(value)
                elif param == 'SRATE':
                    self.srate = int(value)
                self.win_size = self.srate * self.length
                self.buffer.reset(self.win_size)
                self.EEG_monitor.redraw(self.win_size)

    def add_marker(self, mark):
        if self.io.file_created:
            # Use signal to emit marker annotation
            self.annotation_signal.emit(mark, self.buffer.get_current_instant(), -1)
        self.EEG_monitor.draw_vertical_line(mark)

    def visualize(self):
        self.EEG_monitor.update(self.buffer.get_filtered())
        self.Frequency_monitor.update_spectrum(self.buffer.get_spectral())

    def select_mode(self):
        self.Spectrogram_radioButton_isChecked.value = self.Spectrogram_radioButton.isChecked()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.io.fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "", "JSON Files (*.json)", options=options)

    def openFileNameDialog(self, btn):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileType = "PYTHON Files (*.py)"
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", fileType, options=options)
        #----------------- LOAD AND EXECUTE THE MODULE -----#
        self.dyn.load_module(fileName)
