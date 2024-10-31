# -*- coding: utf-8 -*-
"""
@author: Mikel Val Calvo
@email: mvalcal1@upv.edu.es
@institution: Instituto Universitario de Investigación en Tecnología Centrada en el Ser Humano,
              Universitat Politècnica de València, València, Spain
"""

# Import the trigger_client class
from COM.trigger_client import TriggerClient  # Replace with the actual filename if different

import time

def main():
    # Initialize the client with localhost and port 10000
    client = TriggerClient(address="localhost", port=10000)

    # Create the socket
    client.create_socket()

    # Connect to the server
    client.connect()

    # Send a message to the server
    message = "SHOW".encode()  # Make sure to encode the message to bytes
    client.send_msg(message)

    time.sleep(2)

    # Send a message to the server
    message = "LABEL_1".encode()  # Make sure to encode the message to bytes
    client.send_msg(message)

    time.sleep(2)

    # Send a message to the server
    message = "SHOW".encode()  # Make sure to encode the message to bytes
    client.send_msg(message)

    # Close the socket connection
    client.close_socket()


if __name__ == "__main__":
    main()
