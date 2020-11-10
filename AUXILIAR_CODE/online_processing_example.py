# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 10.5281/zenodo.3759306 
"""
from PyQt5 import QtCore 

class MyClass(QtCore.QThread):

    def __init__(self, current_GUI):
        super(MyClass, self).__init__(None)
        self.current_GUI = current_GUI
        self.current_GUI.dmg.FILTERS.append(self.myfilter)
        
    def run(self):
        print(self.current_GUI)
        
    def myfilter(self, sample):
        print('mi filtrado', self.current_GUI)
        return sample