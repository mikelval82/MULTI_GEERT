# -*- coding: utf-8 -*-
"""
@author: Mikel Val Calvo
@email: mvalcal1@upv.edu.es
@institution: Instituto Universitario de Investigación en Tecnología Centrada en el Ser Humano,
              Universitat Politècnica de València, València, Spain
"""

from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence

class EEG_shortcuts:
    
    def __init__(self, parent):
        self.sequences = []
        self.parent = parent
        
    def define_local_shortcuts(self, run_callback, add_marker_callback):
        sequence = {
            'Ctrl+s': lambda:  run_callback('SHOW'),
            'Ctrl+r': lambda:  run_callback('RECORD'),
            'Alt+0': lambda:  add_marker_callback('Label_0'),
            'Alt+1': lambda:  add_marker_callback('Label_1'),
            'Alt+2': lambda:  add_marker_callback('Label_2'),
            'Alt+3': lambda:  add_marker_callback('Label_3'),
            'Alt+4': lambda:  add_marker_callback('Label_4'),
            'Alt+5': lambda:  add_marker_callback('Label_5'),
            'Alt+6': lambda:  add_marker_callback('Label_6'),
            'Alt+7': lambda:  add_marker_callback('Label_7'),
            'Alt+8': lambda:  add_marker_callback('Label_8'),
            'Alt+9': lambda:  add_marker_callback('Label_9'),
        }
        for key, value in list(sequence.items()):
            s = QShortcut(QKeySequence(key),self.parent, value)
            self.sequences.append(s)
    