# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""

from PyQt5 import QtCore 

from pylsl import StreamInlet, resolve_stream

class StreamerLSL(QtCore.QThread):
    log_emitter = QtCore.pyqtSignal(str)
    
    def __init__(self):
        super(StreamerLSL, self).__init__(None)

    def create_lsl(self):
        self.inlets = []
        streams = resolve_stream()

        if streams:
            self.inlets = [StreamInlet(stream) for stream in streams]
            self.log_emitter.emit('Streams resolved!')
            return self.inlets
            
    
          
          
      
    



   