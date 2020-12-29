# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""
import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from QTDesigner.M_GEERT_QT import Ui_M_GEERT as UI
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
        self.MainRecord_btn.clicked.connect(self.main_recording)
        self.TCPIP_checkBox.toggled.connect(self.launch_trigger_server)
        self.Host_LineEdit.textChanged.connect(lambda: self.constants.update('ADDRESS', self.Host_LineEdit.text()))
        self.Port_LineEdit.textChanged.connect(lambda: self.constants.update('PORT', self.Port_LineEdit.text()))
        self.ResolveStreaming_btn.clicked.connect(self.launch_lsl)
        self.Activate_btn.clicked.connect(self.launch_monitor)
        self.Hide_btn.clicked.connect(self.hide)
        self.Run_btn.clicked.connect(lambda:  self.dyn.load_module(self.Scripts_List.currentItem().text()))
        self.Save_btn.clicked.connect(self.dyn.save_script)
        #-------- slots -----------
        self.constants.log_emitter.connect(self.log.myprint)
        #------ show ----------
        self.show()

    def launch_lsl(self):
        self.Streamings_List.clear()
        for inlet in self.lsl.create_lsl():
            item = QtGui.QListWidgetItem(inlet.info().name())
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            item.setCheckState(Qt.Unchecked)
            self.Streamings_List.addItem(item)
            
    def main_recording(self):
        if self.monitors:
            for monitor in self.monitors:
                monitor.run(('RECORD'))
        
    def launch_monitor(self):
        if not self.monitors and self.lsl.inlets:
            # -- check inlets selected ---
            self.inlets = []
            for inlet, index in zip(self.lsl.inlets, range(len(self.lsl.inlets))):
                if self.Streamings_List.item(index).checkState():
                    self.inlets.append( inlet )
            # -- run data acquirer ---
            self.acq = data_acquirer(self.inlets)
            self.acq.set_up()  
            self.acq.start()
            # --- run monitors to visualice signals ----
            for i in range(len(self.acq.buffers['inlet'])):
                if self.acq.buffers['inlet'][i].info().type() == 'EEG':
                    monitor = EEG_monitor_wrapper(self.log, self.acq.buffers['inlet'][i], self.acq.buffers['buffer'][i], 
                                                              self.acq.buffers['counter'][i], self.acq.buffers['streaming'][i], 
                                                              self.acq.buffers['active'][i])
                    monitor.show()
                    self.monitors.append( monitor )    
        else:
            #---- kill data acquirer and close all activef monitors -----
            for monitor in self.monitors:
                try:
                    monitor.closeEvent(None) 
                except:
                    print('No monitor!!')
            self.monitors=[]
            
    def hide(self):
        if self.monitors:
            for monitor in self.monitors:
                if monitor.is_shown:
                    monitor.hide()
                    monitor.is_shown = False
                    self.Hide_btn.setStyleSheet('QPushButton {background-color: #424242; color: #fff;}')
                    self.Hide_btn.setText('Show')
                elif not monitor.is_shown:
                    monitor.show()
                    monitor.is_shown = True
                    self.Hide_btn.setStyleSheet('QPushButton {background-color: #transparent; color: #ff732d;}')
                    self.Hide_btn.setText('Hide')
        
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
        
    
        
        
      





 




