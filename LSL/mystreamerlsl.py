'''
  streamerlsl.py
  ---------------

  This is the module that handles the creation and function of LSL using OpenBCI data.
  
  If the GUI application is used, the GUI controls the parameters of the stream, and calls
  the functions of this class to create, run, and stop each stream instance.

  If the command line application is used, this module creates the LSL instances
  using default parameters, and then allows the user interaction with the stream via the CLI.


'''
from PyQt5 import QtCore 

from pylsl import StreamInlet, resolve_stream

class StreamerLSL(QtCore.QThread):
    log_emitter = QtCore.pyqtSignal(str)
    
    def __init__(self):
        super(StreamerLSL, self).__init__(None)

    def create_lsl(self):
        self.inlets = []
        streams = resolve_stream('type', 'EEG')

        if streams:
            self.inlets = [StreamInlet(stream) for stream in streams]
            self.log_emitter.emit('Streams resolved!')
            return self.inlets
            
    
          
          
      
    



   