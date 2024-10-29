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


def generate_wave(A, B, f, t, wave_type, phi=0, num_channels=8, noise_level=0.0):
    """Genera una onda cuadrada o sinusoidal con una fase opcional."""
    if wave_type == 'square':
        # Generar onda cuadrada con fase
        sample = [A * np.sign(np.sin(2 * np.pi * f * t + phi)) + B + noise_level * np.random.randn() for _ in range(num_channels)]
    elif wave_type == 'sinusoidal':
        # Generar onda sinusoidal con fase
        sample = [A * np.sin(2 * np.pi * f * t + phi) + B + noise_level * np.random.randn() for _ in range(num_channels)]
    else:
        raise ValueError("Tipo de onda no reconocido. Usa 'square' o 'sinusoidal'.")
    return sample


def main(*args):
    if len(args[0]) < 3:
        print("Por favor, proporciona el tipo de onda ('square' o 'sinusoidal'), el nombre de la señal y la fase (en radianes).")
        return

    wave_type = args[0][0]  # Tipo de onda (square o sinusoidal)
    stream_name = args[0][1]  # Nombre de la señal (para diferenciar los streams)
    phi = float(args[0][2])  # Fase de la onda (en radianes)

    # Create stream info for the LSL outlet
    info = StreamInfo(stream_name, 'EEG', 8, 250, 'float32', 'uid_' + stream_name)

    # Add metadata for the stream
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

    # Create an outlet for the monitor (stream)
    outlet = StreamOutlet(info)

    # Parameters for wave generation
    A = 50  # Amplitude
    B = 0  # Offset
    f = 10  # Frequency (Hz) - To maintain coherence, both streams need to have the same frequency
    t = 0  # Initial time
    dt = 1 / 250  # Time step (sampling rate of 250 Hz)
    noise_level = 20.0  # Noise level to add some variability to the signal

    while True:
        # Generate the wave (square or sinusoidal) with the provided phase
        sample = generate_wave(A, B, f, t, wave_type, phi=phi, noise_level=noise_level)
        outlet.push_sample(sample)
        t += dt  # Increment time
        time.sleep(dt)  # Sleep for the sampling period (1/250 seconds)


if __name__ == '__main__':
    main(sys.argv[1:])
