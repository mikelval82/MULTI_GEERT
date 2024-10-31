# -*- coding: utf-8 -*-
"""
@author: Mikel Val Calvo
@email: mvalcal1@upv.edu.es
@institution: Instituto Universitario de Investigación en Tecnología Centrada en el Ser Humano,
              Universitat Politècnica de València, València, Spain
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
            
    
          
          
      
    



   