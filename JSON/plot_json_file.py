# -*- coding: utf-8 -*-
"""
@author: Mikel Val Calvo
@email: mvalcal1@upv.edu.es
@institution: Instituto Universitario de Investigación en Tecnología Centrada en el Ser Humano,
              Universitat Politècnica de València, València, Spain
"""

# Import necessary libraries
import json
import matplotlib.pyplot as plt
import numpy as np


# Function to open and plot the JSON file with annotations
def open_and_plot_json(file_path):
    # Load the JSON file
    print("Loading JSON file...")
    with open(file_path, 'r') as f:
        json_data = json.load(f)

    # Extract signal data and time stamps
    signal_data = json_data['signal_data']
    sampling_rate = json_data['sampling_rate']
    start_time = json_data['start_time']

    # Extracting the signal data into a NumPy array
    num_channels = len(signal_data)
    num_samples = len(signal_data[0]['data'])

    data = np.zeros((num_samples, num_channels))

    for i, channel in enumerate(signal_data):
        data[:, i] = np.array(channel['data'])

    # Create the time stamps based on the sampling rate
    time_stamps = np.linspace(start_time, start_time + num_samples / sampling_rate, num_samples)

    print(f"Data shape: {data.shape}")

    # Plotting each channel (row of the data)
    plt.figure(figsize=(10, 6))

    for i in range(num_channels):
        plt.plot(time_stamps, data[:, i], label=f'Channel {signal_data[i]["channel_label"]}')

    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (µV)")
    plt.title(f"Plot of {num_channels} Channels from JSON File")
    plt.legend(loc="upper right")

    # Check for annotations and plot them if they exist
    if "annotations" in json_data and len(json_data["annotations"]) > 0:
        annotations = json_data["annotations"]
        for annotation in annotations:
            # Convert annotation instant (samples) to time (seconds)
            ann_time = start_time + annotation["instant"] / sampling_rate
            print(annotation)
            event_label = annotation["event"]
            plt.axvline(x=ann_time, color='r', linestyle='--', label=f'Annotation: {event_label}')
            plt.text(ann_time, plt.ylim()[1], event_label, rotation=90, color='red')

    plt.show()


# Example usage
file_path = 'signal_1_Trial_0.json'
open_and_plot_json(file_path)
