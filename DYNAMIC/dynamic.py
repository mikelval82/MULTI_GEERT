# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""
        
import sys 
import os
from PyQt5 import QtCore 

from os import listdir
from os.path import isfile, join
import importlib
#from importlib import reload

class dynamic(QtCore.QThread):
    log_emitter = QtCore.pyqtSignal(str)
    
    def __init__(self, current_GUI, listWidget, RawCode):
        super(dynamic, self).__init__(None)
        self.current_GUI = current_GUI
        self.RawCode = RawCode
        self.listWidget = listWidget
        self.current_row = 0

    def load_module(self, fileName):
        ########### separo path y nombre del modulo ##############
        aux = fileName.split("/")
        path = ''
        for i in range(1, len(aux)-1):
            path += aux[i] + '/'
        module_name = aux[-1][:-3]
        #---------------------------------------------------------
        sys.path.append(os.path.realpath('./AUXILIAR_CODE/'))

        try:
            module = importlib.import_module(module_name)
            my_class = getattr(module, 'MyClass')
            self.my_instance = my_class(self.current_GUI)
            self.my_instance.start()
            self.log_emitter.emit('DONE!')
        except:
            self.log_emitter.emit('Cannot load the module!')
            
    def save_script(self):
        script = self.listWidget.currentItem().text()
        code = self.RawCode.toPlainText()
        # open file in write mode
        f=open("./AUXILIAR_CODE/" + script, "w")
        f.write(code)
        f.flush()
        f.close()   
        # update values
        self.load_auxiliar_code()      
        self.edited = True
              
    def load_auxiliar_code(self):
        self.listWidget.clear()
        mypath = './AUXILIAR_CODE/'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for file in onlyfiles:
            self.listWidget.addItem(file)
            
        self.listWidget.itemClicked.connect(self.show_code)
        
        self.listWidget.setCurrentRow(self.current_row)
        self.show_code(self.listWidget.currentItem())
        
    def show_code(self, scriptItem):
        # read the file
        f=open("./AUXILIAR_CODE/" + scriptItem.text(), "r")
        contents =f.read()
        f.close()
        # update code viewer
        self.RawCode.setPlainText( contents )
        self.current_row = self.listWidget.currentRow() 
          
