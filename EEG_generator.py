# -*- coding: utf-8 -*-
"""
@author: Mikel Val Calvo
@email: mvalcal1@upv.edu.es
@institution: Instituto Universitario de Investigación en Tecnología Centrada en el Ser Humano,
              Universitat Politècnica de València, València, Spain
"""

from pylsl import StreamInfo, StreamOutlet
import numpy as np
import time
import sys
from argparse import ArgumentParser


def generate_wave(A, B, f, t, wave_type, phi=0, num_channels=8, noise_level=0.0, chirp_speed=1.0):
    """Genera una onda cuadrada, sinusoidal o chirp con una fase opcional.
    - f: Frecuencia base cuando t=0
    - chirp_speed: La velocidad de cambio en frecuencia para la onda tipo chirp
    """
    if wave_type == 'square':
        # Generar onda cuadrada con fase
        sample = [A * np.sign(np.sin(2 * np.pi * f * t + phi)) + B for _ in range(num_channels)]
    elif wave_type == 'sinusoidal':
        # Generar onda sinusoidal con fase
        sample = [A * np.sin(2 * np.pi * f * t + phi) + B for _ in range(num_channels)]
    elif wave_type == 'chirp':
        # Aumentar o disminuir la frecuencia linealmente en función del tiempo
        current_freq = f * (1 + chirp_speed * t)  # Frecuencia lineal que cambia con el tiempo
        sample = [A * np.sin(2 * np.pi * current_freq * t + phi) + B for _ in range(num_channels)]
    else:
        raise ValueError("Tipo de onda no reconocido. Usa 'square', 'sinusoidal' o 'chirp'.")

    # Añadir el ruido (si está habilitado)
    if noise_level != 0.0:
        sample = [s + noise_level * np.random.randn() for s in sample]

    return sample


def parse_arguments():
    """Parsea los argumentos de línea de comandos."""
    parser = ArgumentParser(description="Generador de señales EEG (ondas 'square', 'sinusoidal' o 'chirp')")
    parser.add_argument('wave_type', type=str, choices=['square', 'sinusoidal', 'chirp'],
                        help="Tipo de onda: 'square', 'sinusoidal' o 'chirp'")
    parser.add_argument('stream_name', type=str, help="Nombre del stream para diferenciar los flujos de datos")
    parser.add_argument('phi', type=float, help="Fase de la onda en radianes")
    parser.add_argument('--chirp_speed', '-cs', type=float, default=1.0,
                        help="Velocidad de chirp para controlar la aceleración de frecuencia en el modo 'chirp'. Valor por defecto: 1.0")
    parser.add_argument('--frequency', '-f', type=float, default=10.0,
                        help="Frecuencia base de la señal (Hz). Valor por defecto: 10 Hz.")
    parser.add_argument('--sampling_rate', '-sr', type=float, default=250.0,
                        help="Tasa de muestreo en Hz. Valor por defecto: 250 Hz.")
    parser.add_argument('--amplitude', '-A', type=float, default=50.0,
                        help="Amplitud de la onda. Valor por defecto: 50")
    parser.add_argument('--offset', '-B', type=float, default=0.0,
                        help="Desplazamiento de la señal. Valor por defecto: 0")
    parser.add_argument('--noise_level', '-n', type=float, default=20.0,
                        help="Nivel de ruido (desviación estándar). Valor por defecto: 20")
    return parser.parse_args()


def main():
    args = parse_arguments()

    # Crear la información del stream para la salida LSL
    info = StreamInfo(args.stream_name, 'EEG', 64, args.sampling_rate, 'float32', 'uid_' + args.stream_name)

    # Añadir metadatos del flujo
    chns = info.desc().append_child("channels")
    for label in ["C3", "C4", "Cz", "FPz", "POz", "CPz", "O1", "O2"]*8:
        ch = chns.append_child("channel")
        ch.append_child_value("label", label)
        ch.append_child_value("unit", "microvolts")
        ch.append_child_value("type", "EEG")
    info.desc().append_child_value("manufacturer", "SCCN")
    cap = info.desc().append_child("cap")
    cap.append_child_value("name", "EasyCap")
    cap.append_child_value("size", "54")
    cap.append_child_value("labelscheme", "10-20")

    # Crear la salida para el monitor (stream)
    outlet = StreamOutlet(info)

    A = args.amplitude
    B = args.offset
    f = args.frequency
    t = 0
    dt = 1 / args.sampling_rate
    noise_level = args.noise_level

    try:
        while True:
            # Generar la onda y controlar la aceleración con chirp_speed (si es un chirp)
            sample = generate_wave(A, B, f, t, args.wave_type, phi=args.phi, num_channels=64, noise_level=noise_level,
                                   chirp_speed=args.chirp_speed)
            outlet.push_sample(sample)
            t += dt  # Incremento de tiempo
            time.sleep(dt)  # Esperar un período de muestreo (1/250 segundos)
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
        sys.exit(0)


if __name__ == '__main__':
    main()
