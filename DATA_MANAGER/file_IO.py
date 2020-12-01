# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""
from EDF.writeEDFFile import edf_writter
from multiprocessing import Process

class io_manager:
    
    def __init__(self):
        self.edf = edf_writter()
        self.fileName = 'unknown'
        self.Trial = 0
        self.file_created = False
        
    def create_file(self):
        self.edf.new_file(self.fileName + '_Trial_' + str(self.Trial) + '.edf')
        self.file_created = True
        
    def close_file(self):
        self.edf.close_file()
        self.Trial+=1
        self.file_created = False
        
    def append_to_file(self, stream):
        self.edf.append(stream)
        p = Process(target=self.edf.writeToEDF())
        p.start()
    
    def online_annotation(self, event, instant, duration = -1):
        self.edf.annotation(instant, duration, event)
