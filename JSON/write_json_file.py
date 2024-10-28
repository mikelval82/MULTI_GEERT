# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""
import numpy as np
import os
import time
import datetime
import json


class JSONWriter:

    def __init__(self, CHANNELS=8, CHANNEL_IDS=['Fp1', 'Fp2', 'T1', 'T2', 'O1', 'O2', 'P1', 'P2'], SAMPLE_RATE=250):
        self.CHANNELS = CHANNELS
        self.CHANNEL_IDS = CHANNEL_IDS
        self.SAMPLE_RATE = SAMPLE_RATE

        # Initialize metadata dictionary
        self.metadata = {
            "channels": self.CHANNEL_IDS,
            "sampling_rate": self.SAMPLE_RATE,
            "start_time": time.time(),
            "date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "signal_data": [],
            "annotations": []
        }

    def new_file(self, path):
        self.file_path = os.path.join('.', path)
        self.metadata["file_name"] = self.file_path
        print(f"New JSON file created at: {self.file_path}")

    def append(self, all_data_store):
        print(f"Appending data of shape {all_data_store.shape}")
        # For each channel, append its signal data
        for channel in range(self.CHANNELS):
            ch_signal = all_data_store[channel, :]
            # Append signal data to the metadata
            self.metadata["signal_data"].append({
                "channel_label": self.CHANNEL_IDS[channel],
                "data": ch_signal.tolist()  # Convert NumPy array to list for JSON compatibility
            })
            print(f"Channel: {self.CHANNEL_IDS[channel]}, min: {ch_signal.min()}, max: {ch_signal.max()}")

    def annotation(self, instant, duration, event):
        # Add the annotation details to the metadata
        self.metadata["annotations"].append({
            "instant": instant,
            "duration": duration,
            "event": event
        })
        print(f"Annotation added: {event} at {instant} seconds, duration: {duration}")

    def write_to_json(self):
        # Write signal data and annotations into a .json file to simulate saving the data in JSON format.
        data_to_save = {
            "signal_data": self.metadata["signal_data"],
            "annotations": self.metadata["annotations"],
            "start_time": self.metadata["start_time"],
            "sampling_rate": self.metadata["sampling_rate"],
            "channels": self.metadata["channels"]
        }

        # Save the file as a .json file (this can be adapted to another format if needed)
        with open(self.file_path, 'w') as outfile:
            json.dump(data_to_save, outfile, indent=4)

        print(f"JSON file saved at: {self.file_path}")

    def close_file(self):
        self.metadata["end_time"] = time.time()
        print(f"Closing file: {self.file_path}")

    def __del__(self):
        print("Deleted JSONWriter instance")

