# -*- coding: utf-8 -*-
"""
@author: Mikel Val Calvo
@email: mvalcal1@upv.edu.es
@institution: Instituto Universitario de Investigación en Tecnología Centrada en el Ser Humano,
              Universitat Politècnica de València, València, Spain
"""

import numpy as np  # Missing import for numpy
from JSON.write_json_file import JSONWriter
from multiprocessing import Process


class io_manager:

    def __init__(self, monitor_ID):
        self.fileName = './Data/' + monitor_ID
        self.Trial = 0
        self.file_created = False
        self.json = None

    def create_file(self):
        # Create new file with correct trial number
        self.json = JSONWriter()
        self.json.new_file(self.fileName + '_Trial_' + str(self.Trial) + '.json')
        self.file_created = True

    def close_file(self):
        # Close the current file and increment the trial counter
        self.json.close_file()
        self.Trial += 1
        self.file_created = False

    def append_to_file(self, stream):
        # Ensure the stream is transposed and in contiguous memory for performance
        transposed = np.ascontiguousarray(stream.T)
        # Append the transposed stream to the JSON file
        self.json.append(transposed)
        # Start the process to write the data to the JSON file asynchronously
        p = Process(target=self.json.write_to_json)
        p.start()

    def online_annotation(self, event, instant, duration=-1):
        # Add an annotation to the JSON file
        self.json.annotation(instant, duration, event)
