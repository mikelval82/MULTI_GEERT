# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 
"""
import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from QTDesigner.M_GEERT_QT import Ui_M_GEERT as UI
from multiprocessing import Value
from GUI.EEG_monitor_wrapper import EEG_monitor_wrapper 
from UTILITIES.GLOBAL import constants
from LOGGING.logger import logger
from COM.trigger_server_2 import trigger_server
from DYNAMIC.dynamic import dynamic
from LSL.mystreamerlsl import StreamerLSL
from DATA_MANAGER.data_acquirer import data_acquirer

class GUI(QMainWindow, UI):
    def __init__(self):
        QMainWindow.__init__(self, parent=None) 
        #----- gui settings -----------
        self.setupUi(self)
        self.log = logger(self.Logger)
        self.constants = constants()
        self.dyn = dynamic(self, self.Scripts_List, self.Code_TextEdit)#None hay que cambiarlo por el acceso a los streams!!!!!!
        self.dyn.log_emitter.connect(self.log.myprint)
        self.dyn.load_auxiliar_code()
        self.lsl = StreamerLSL()
        self.lsl.log_emitter.connect(self.log.myprint)
        #-------- Monitors List ---
        self.monitors = []
        #-------- controls --------
        self.trigger_server_activated = False
        #-------- connections ----
        self.Experiment_btn.clicked.connect(self.saveFileDialog)
        self.MainRecord_btn.clicked.connect(lambda: self.main_recording('RECORD'))
        
        self.TCPIP_checkBox.toggled.connect(self.launch_trigger_server)
        self.Host_LineEdit.textChanged.connect(lambda: self.constants.update('ADDRESS', self.Host_LineEdit.text()))
        self.Port_LineEdit.textChanged.connect(lambda: self.constants.update('PORT', self.Port_LineEdit.text()))
        
        self.ResolveStreaming_btn.clicked.connect(self.launch_lsl)
        self.Activate_btn.clicked.connect(self.launch_monitor)
        
        self.Run_btn.clicked.connect(lambda:  self.dyn.load_module(self.Scripts_List.currentItem().text()))
        self.Save_btn.clicked.connect(self.dyn.save_script)
        #-------- slots -----------
        self.constants.log_emitter.connect(self.log.myprint)
        #------ show ----------
        self.show()

    def launch_lsl(self):
        self.Streamings_List.clear()
        for inlet in self.lsl.create_lsl():#~ aqui hay que comprobar si ya los teníamos en la lista, diccionarios??
            item = QtGui.QListWidgetItem(inlet.info().name())
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            item.setCheckState(Qt.Unchecked)
            self.Streamings_List.addItem(item)
        
    def launch_monitor(self):
        if not self.monitors and self.lsl.inlets:
            self.inlets = []
            for inlet, index in zip(self.lsl.inlets, range(len(self.lsl.inlets))):
                if self.Streamings_List.item(index).checkState():
                    self.inlets.append( inlet )
            
            self.acq = data_acquirer(self.inlets)
            self.acq.set_up(8, 1500, 250)
            self.acq.start()
            
            for inlet, buffer, counter, recording in zip(self.acq.buffers['inlet'], self.acq.buffers['buffer'], self.acq.buffers['counter'], self.acq.buffers['recording']):
                self.monitors.append( EEG_monitor_wrapper(inlet.info(), buffer, counter, recording) )
            print('create', self.monitors, self.inlets)
        else:
            self.acq.kill()
            [monitor.closeEvent(None) for monitor in self.monitors]
            self.monitors=[]
            print('killing', self.monitors, self.inlets)
                
        
    def launch_trigger_server(self):
        if self.trigger_server_activated:
            self.trigger_server.close_socket()
            del self.trigger_server
            self.trigger_server_activated = False
        else:
            self.trigger_server = trigger_server(self.constants)
            self.trigger_server.log_emitter.connect(self.log.myprint_out)
            self.trigger_server.socket_emitter.connect(self.main_recording)
            self.trigger_server_activated = self.trigger_server.create_socket()
            if self.trigger_server_activated:
                self.trigger_server.start()  
            else:
                del self.trigger_server
                self.TCPIP_checkBox.setChecked(False)
                
    def main_recording(self, action):
        if self.monitors:
            for monitor in self.monitors:
                monitor.run(action)
        elif self.lsl.inlets:
            for inlet, i in zip(self.lsl.inlets, range(0,len(self.lsl.inlets))):
                if self.Streamings_List.item(i).checkState():
                    monitor = EEG_monitor_wrapper(inlet)
                    monitor.run(action)
                    self.monitors.append(monitor)
        
    def saveFileDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, filetype = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","(*.npy)", options=options)
        try:
            os.mkdir(fileName)
            self.constants.update('experiment', fileName)
        except OSError:
            self.log.myprint_error ("Creation of the directory %s failed" % fileName)
        else:
            self.log.myprint_out ("Successfully created the directory %s " % self.constants.experiment)
        
    
        
        
      





 




