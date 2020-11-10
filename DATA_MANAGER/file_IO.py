# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 
"""
from EDF.writeEDFFile import edf_writter
from multiprocessing import Process

class io_manager:
    
    def __init__(self):
        self.edf = edf_writter()
        self.ispath = False
        
    def create_file(self, PATH='sujeto'):
        self.edf.new_file(PATH + '.edf')
        self.ispath = True
        
    def close_file(self):
        if self.ispath:
            self.edf.close_file()
        
    def append_to_file(self, stream):
        if self.ispath:
            self.edf.append(stream)
            p = Process(target=self.edf.writeToEDF())
            p.start()
    
    def online_annotation(self, event, instant, duration = -1):
        if self.ispath:
            self.edf.annotation(instant, duration, event)
