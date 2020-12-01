# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""
from multiprocessing import Process

#from datetime import datetime
#import time

class VIDEO_data_processing(Process):
    
    def __init__(self, event, buffer):
        Process.__init__(self)
        self.event = event
        self.buffer = buffer
#        self.old = datetime.now().timestamp() * 1000
 
    def run(self):  
        while self.event.wait():
#            time.sleep(1)
            #################### DEFAULT FILTERING PROCESS ####################
            sample = self.buffer.get()
            filtered = self.default_filtering( sample )
            self.buffer.set_filtered(filtered)
            ###################################################################
            #******************************************************************
#            new = datetime.now().timestamp() * 1000
#            print(self.name, ' processing: ', new-self.old)
#            self.old = new
            
    def default_filtering(self, data):
        ######## add filtering processes ########################
        return data
                


        

  
    


        
                
    