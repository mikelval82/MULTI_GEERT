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


def generate_wave(A, B, f, t, wave_type, num_channels=8):
    """Genera una onda cuadrada o sinusoidal según el tipo especificado."""
    if wave_type == 'square':
        # Generar onda cuadrada
        sample = [A * np.sign(np.sin(2 * np.pi * f * t)) + B for _ in range(num_channels)]
    elif wave_type == 'sinusoidal':
        # Generar onda sinusoidal
        sample = [A * np.sin(2 * np.pi * f * t) + B for _ in range(num_channels)]
    else:
        raise ValueError("Tipo de onda no reconocido. Usa 'square' o 'sinusoidal'.")
    return sample


def main(*args):
    print(args, len(args))
    if len(args[0]) < 2:
        print("Por favor, proporciona el tipo de onda: 'square' o 'sinusoidal'.")
        return

    wave_type = args[0][0]  # Tipo de onda (square o sinusoidal)

    # first create a new stream info (here we set the name to BioSemi,
    # the content-type to EEG, 8 channels, 100 Hz, and float-valued data) The
    # last value would be the serial number of the device or some other more or
    # less locally unique identifier for the stream as far as available (you
    # could also omit it but interrupted connections wouldn't auto-recover)

    info = StreamInfo(args[0][1], 'EEG', 8, 250, 'float32', 'myuid34234')
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

    # Parameters for wave generation
    A = 50  # Amplitude
    B = 0  # Offset
    f = 1  # Frequency (Hz)
    t = 0  # Initial time
    dt = 1 / 250  # Time step (sampling rate of 250 Hz)

    while True:
        # Generate the wave (square or sinusoidal)
        sample = generate_wave(A, B, f, t, wave_type)
        outlet.push_sample(sample)
        t += dt  # Increment time
        time.sleep(dt)  # Sleep for the sampling period (1/250 seconds)


if __name__ == '__main__':
    main(sys.argv[1:])
