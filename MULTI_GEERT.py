# -*- coding: utf-8 -*-
"""
@author: Mikel Val Calvo
@email: mvalcal1@upv.edu.es
@institution: Instituto Universitario de Investigación en Tecnología Centrada en el Ser Humano,
              Universitat Politècnica de València, València, Spain
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
        with open("QTDesigner/CSS/Genetive.qss") as f:
            self.setStyleSheet(f.read())

if __name__ == '__main__':
    main = MULTI_GEERT()
