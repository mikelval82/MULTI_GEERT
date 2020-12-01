# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""
from PyQt5 import QtCore 

class constants(QtCore.QThread):
    log_emitter = QtCore.pyqtSignal(str)
    
    def __init__(self):
        super(constants, self).__init__(None)
        self.experiment = './experiment'
        self.ADDRESS = 'localhost'
        self.PORT = 10000
        
    def update(self, param, value):
        if param == 'experiment':
            self.experiment = value
        elif param == 'ADDRESS':
            self.ADDRESS = value
        elif param == 'PORT':
            self.PORT = value
        
        self.log_emitter.emit('Updated param: ' + param + ' value: ' + value)
        