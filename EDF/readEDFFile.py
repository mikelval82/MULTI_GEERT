# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 10.5281/zenodo.3759306 
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
