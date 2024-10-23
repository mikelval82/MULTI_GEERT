# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""

import numpy as np  # Missing import for numpy
from JSON.write_json_file import JSONWriter
from multiprocessing import Process


class io_manager:

    def __init__(self, monitor_ID):
        self.xdf = JSONWriter()
        self.fileName = monitor_ID
        self.Trial = 0
        self.file_created = False

    def create_file(self):
        # Create new file with correct trial number
        self.xdf.new_file(self.fileName + '_Trial_' + str(self.Trial) + '.xdf')
        self.file_created = True

    def close_file(self):
        # Close the current file and increment the trial counter
        self.xdf.close_file()
        self.Trial += 1
        self.file_created = False

    def append_to_file(self, stream):
        # Ensure the stream is transposed and in contiguous memory for performance
        transposed = np.ascontiguousarray(stream.T)
        print('file io, append to file, transposed stream shape: ', transposed.shape)

        # Print min, max, mean, and std of each signal (channel)
        for signal in transposed:
            print(signal.min(), signal.max(), signal.mean(), signal.std())

        # Append the transposed stream to the JSON file
        self.xdf.append(transposed)

        # Start the process to write the data to the JSON file asynchronously
        p = Process(target=self.xdf.write_to_json)  # Fixing method name: writeToXDF instead of writeToEDF
        p.start()

    def online_annotation(self, event, instant, duration=-1):
        # Add an annotation to the JSON file
        self.xdf.annotation(instant, duration, event)
