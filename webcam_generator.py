# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
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
    info = StreamInfo(args[0][0], 'video', 640*480, 25, 'float32', 'myuid34234')
    outlet = StreamOutlet(info)

    while True:
        outlet.push_sample( np.reshape(np.random.rand(640,480), (640*480,)) )
        time.sleep(1/25)


if __name__ == '__main__':
    main(sys.argv[1:])