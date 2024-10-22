# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Biomedical Neuroengineering Research Group (UMH); Biomedical Neuroengineering Research Group (UMH) ) 
@DOI: 
"""
from GUI.M_GEERT_gui import GUI 

from PyQt5.QtWidgets import QApplication
import sys

class MULTI_GEERT(QApplication):
    def __init__(self):
        QApplication.__init__(self,[''])
        self.load_style()
        #--- Launch GUI ---
        self.gui = GUI()
        #--- exec ---
        sys.exit(self.exec_())
        
    def load_style(self):        
        with open("QTDesigner/CSS/Adaptic.qss") as f:
            self.setStyleSheet(f.read())

if __name__ == '__main__':
    main = MULTI_GEERT()
