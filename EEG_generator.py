# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""


from pylsl import StreamInfo, StreamOutlet
import numpy as np
import time
import sys

def main(*args):
    # first create a new stream info (here we set the name to BioSemi,
    # the content-type to EEG, 8 channels, 100 Hz, and float-valued data) The
    # last value would be the serial number of the device or some other more or
    # less locally unique identifier for the stream as far as available (you
    # could also omit it but interrupted connections wouldn't auto-recover)

    info = StreamInfo(args[0][0], 'EEG', 8, 250, 'float32', 'myuid34234')
    # now attach some meta-data (in accordance with XDF format,
    # see also code.google.com/p/xdf)
    chns = info.desc().append_child("channels")
    for label in ["C3", "C4", "Cz", "FPz", "POz", "CPz", "O1", "O2"]:
        ch = chns.append_child("channel")
        ch.append_child_value("label", label)
        ch.append_child_value("unit", "microvolts")
        ch.append_child_value("type", "EEG")
    info.desc().append_child_value("manufacturer", "SCCN")
    cap = info.desc().append_child("cap")
    cap.append_child_value("name", "EasyCap")
    cap.append_child_value("size", "54")
    cap.append_child_value("labelscheme", "10-20")
    # next make an outlet
    outlet = StreamOutlet(info)

    while True:
        outlet.push_sample(np.random.rand(8)*100)
        time.sleep(1/250)


if __name__ == '__main__':
    main(sys.argv[1:])