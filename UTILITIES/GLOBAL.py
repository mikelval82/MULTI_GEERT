# -*- coding: utf-8 -*-
"""
@author: Mikel Val Calvo
@email: mvalcal1@upv.edu.es
@institution: Instituto Universitario de Investigación en Tecnología Centrada en el Ser Humano,
              Universitat Politècnica de València, València, Spain
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
        