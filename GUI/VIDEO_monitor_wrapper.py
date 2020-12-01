# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""
from multiprocessing import Event
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import numpy as np

from VIDEO_IO import AudioVisual_IO
from QTDesigner.VIDEO_monitor import Ui_MainWindow as UI
from DATA_MANAGER.VIDEO_data_processing import VIDEO_data_processing
from DYNAMIC.dynamic import dynamic
from GUI.VIDEO_monitor_shortcuts_manager import VIDEO_shortcuts

class VIDEO_monitor_wrapper(QMainWindow, UI):
    
    def __init__(self, inlet, buffer, counter, streaming, active):
        QMainWindow.__init__(self, parent=None)
        #---- GUI setup ----------
        self.setupUi(self)
        self.setWindowTitle(inlet.info().name())      
        self.show()
        # --- buffer related data structures ----
        self.inlet = inlet
        self.buffer = buffer
        self.counter = counter
        self.streaming = streaming
        self.active = active
        #--- global params -----
        self.name = self.inlet.info().name()
        self.win_size = 10# OJO HARDCODING!!!
        self.fileName = ''
        #----- shared variables ------------
        self.event = Event()
        #-----------------------------------------------------------------------------------------------------------
        self.shortcuts = VIDEO_shortcuts(self)
        self.shortcuts.define_local_shortcuts(self.run, self.add_marker)
        #---- streaming processing ----
        self.processing = VIDEO_data_processing(self.event, self.buffer)
        self.processing.start()
        #---- setup monitors ------
        self.viewer.create_plot()
        self.frames = [self.frame_1, self.frame_2, self.frame_3, self.frame_4, self.frame_5, self.frame_6, self.frame_7, self.frame_8, self.frame_9, self.frame_10]
        for frame in self.frames:
            frame.create_plot() 
        #---- dynamic imports ------------
        self.dyn = dynamic(self, None, None)#el primer None hay que cambiarlo por el acceso a los streams!!!!!!
        #---- callbacks ------
        self.Filename_btn.clicked.connect(self.saveFileDialog)
        self.Import_btn.clicked.connect(self.openFileNameDialog)
        self.Start_btn.clicked.connect(lambda: self.run('SHOW'))
        self.Record_btn.clicked.connect(lambda: self.run('RECORD'))
        self.AddMarker_btn.clicked.connect(lambda: self.add_marker(self.Markers_ComboBox.currentText()))
        self.carrousel_horizontalSlider.valueChanged.connect(lambda: self.update_slider(self.carrousel_horizontalSlider.value()))
        self.carrousel_horizontalSlider.setEnabled(False)
        #--- visualize timer ----
        self.timer = QtCore.QTimer()
        self.timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer.timeout.connect(self.visualize)
        self.refresh_rate = 0
        #---- close the sub-app -------
        self.actionQuit = QtWidgets.QAction("Quit", self)
        self.actionQuit.triggered.connect(QtWidgets.QApplication.quit)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)   
  
    def run(self, action):
        if action == 'SHOW' and not self.streaming.value:
            self.buffer.reset()
            self.event.set()
            self.timer.start(self.refresh_rate)
            self.carrousel_horizontalSlider.setEnabled(False)
        elif action == 'SHOW' and self.streaming.value:
            self.event.clear()
            self.timer.stop()
            # --- slider configuration ---
            self.carrousel_horizontalSlider.setMinimum(1)
            self.carrousel_horizontalSlider.setMaximum(self.buffer.get_current_instant()-9)
            self.carrousel_horizontalSlider.setValue(1)
            self.carrousel_horizontalSlider.setEnabled(True)
        elif action == 'RECORD' and not self.streaming.value:
            self.buffer.reset()
            self.event.set()
            self.timer.start(self.refresh_rate)
            self.carrousel_horizontalSlider.setEnabled(False)
        elif action == 'RECORD' and self.streaming.value:
            self.event.clear()
            self.timer.stop()
            AudioVisual_IO.write_AV(self.buffer.get_stream(), self.fileName, 0)
            self.carrousel_horizontalSlider.setEnabled(True)
        self.streaming.value = not self.streaming.value

    def closeEvent(self, event):
        self.active.value = False
        self.processing.kill()
        self.close()
            
    def add_marker(self, mark):
        print(mark)
        frame = np.zeros((640, 480, 3))
        if mark == 'Label_0':
            frame[:,:,0] = .1 
            frame[:,:,1] = .2
            frame[:,:,2] = .3
        elif mark == 'Label_1':
            frame[:,:,0] = .5 
            frame[:,:,1] = .7
            frame[:,:,2] = .2
        elif mark == 'Label_2':
            frame[:,:,0] = .9 
            frame[:,:,1] = .1
            frame[:,:,2] = .4
        elif mark == 'Label_3':
            frame[:,:,0] = .2 
            frame[:,:,1] = .5
            frame[:,:,2] = .8
        elif mark == 'Label_4':
            frame[:,:,0] = .3 
            frame[:,:,1] = .9
            frame[:,:,2] = .4
        elif mark == 'Label_5':
            frame[:,:,0] = .4
            frame[:,:,1] = .9
            frame[:,:,2] = .5
        elif mark == 'Label_6':
            frame[:,:,0] = .2 
            frame[:,:,1] = .8
            frame[:,:,2] = .9
        elif mark == 'Label_7':
            frame[:,:,0] = .5 
            frame[:,:,1] = .7
            frame[:,:,2] = .2
        elif mark == 'Label_8':
            frame[:,:,0] = .9 
            frame[:,:,1] = .7
            frame[:,:,2] = .2
        elif mark == 'Label_9':
            frame[:,:,0] = .1 
            frame[:,:,1] = .3
            frame[:,:,2] = .5
        self.buffer.set_stream_label(frame)

    def visualize(self):
        self.viewer.update( self.buffer.get_filtered() )
        for index, frame in enumerate(self.frames):
            frame.update( self.buffer.get_frame(index) )
       
    def update_slider(self, value):
        self.viewer.update( self.buffer.get_stream(value) )
        for index, frame in enumerate(self.frames):
            frame.update( self.buffer.get_stream(value+index-1) )
        
    def saveFileDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","EDF Files (*.edf)", options=options)            
   
    def openFileNameDialog(self, btn):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileType = "PYTHON Files (*.py)"
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","",fileType, options=options)       
        #----------------- LOAD AND EXECUTE THE MODULE -----#
        self.dyn.load_module(fileName)
      

        
 

        

    