# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""
#%%
from PyQt5 import QtGui, QtCore

class logger():
    def __init__(self, logger):
        self.logger = logger
        self.logger.setCenterOnScroll(True)
        
        self.tf = QtGui.QTextCharFormat()
        self.tf_yellow = QtGui.QTextCharFormat()
        self.tf_green = QtGui.QTextCharFormat()
        self.tf_red = QtGui.QTextCharFormat()
        
        self.tf_yellow.setForeground(QtGui.QBrush(QtCore.Qt.yellow))
        self.tf_green.setForeground(QtGui.QBrush(QtCore.Qt.green))
        self.tf_red.setForeground(QtGui.QBrush(QtCore.Qt.red))

    def myprint(self, text):
        self.logger.setCurrentCharFormat(self.tf)
        self.logger.appendPlainText(text)
        self.logger.centerCursor()
        
    def myprint_in(self, text):
        self.logger.setCurrentCharFormat(self.tf_yellow)
        self.logger.appendPlainText("< "+text)
        self.logger.centerCursor()
    
    def myprint_out(self, text):
        self.logger.setCurrentCharFormat(self.tf_green)
        self.logger.appendPlainText("> "+text)
        self.logger.centerCursor()
        
    def myprint_error(self, text):
        self.logger.setCurrentCharFormat(self.tf_red)
        self.logger.appendPlainText(text)
        self.logger.centerCursor()
        
    def clear(self):
        self.logger.clear()