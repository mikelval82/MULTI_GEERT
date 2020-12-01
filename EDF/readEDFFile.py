# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""

import numpy as np
import pyedflib
import matplotlib.pyplot as plt

if __name__ == '__main__':
#    f = pyedflib.data.test_generator()
    f = pyedflib.edfreader.EdfReader('./experimento_1/openbci_sujeto_1_0.edf')

    annotations = f.readAnnotations()
    for n in np.arange(f.annotations_in_file):
        print("annotation: onset is %f    duration is %s    description is %s" % (annotations[0][n],annotations[1][n],annotations[2][n]))

    buf = f.readSignal(0)
    plt.plot(buf)
    
    f._close()
    del f
