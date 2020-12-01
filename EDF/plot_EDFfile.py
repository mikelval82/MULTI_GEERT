# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""

from __future__ import division, print_function, absolute_import

import numpy as np

import pyedflib


import matplotlib.pyplot as plt


if __name__ == '__main__':
    f = pyedflib.edfreader.EdfReader('./experimento_1/openbci_sujeto_1_0.edf')
    n = f.signals_in_file
    signal_labels = f.getSignalLabels()
    n_min = f.getNSamples()[0]
    sigbufs = [np.zeros(f.getNSamples()[i]) for i in np.arange(n)]
    for i in np.arange(n):
        sigbufs[i] = f.readSignal(i)
        if n_min < len(sigbufs[i]):
            n_min = len(sigbufs[i])
    f._close()
    del f

    n_plot = np.min((n_min, 2000))
    sigbufs_plot = np.zeros((n, n_plot))
    for i in np.arange(n):
        sigbufs_plot[i,:] = sigbufs[i][:n_plot]

    plt.plot(sigbufs_plot[:, :n_plot].T)
