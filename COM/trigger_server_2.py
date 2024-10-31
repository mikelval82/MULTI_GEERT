# -*- coding: utf-8 -*-
"""
@author: Mikel Val Calvo
@email: mvalcal1@upv.edu.es
@institution: Instituto Universitario de Investigación en Tecnología Centrada en el Ser Humano,
              Universitat Politècnica de València, València, Spain
"""

from PyQt5 import QtCore 
import socket

class trigger_server(QtCore.QThread):
    socket_emitter = QtCore.pyqtSignal(str)
    log_emitter = QtCore.pyqtSignal(str)
    
    def __init__(self, constants):
        super(trigger_server, self).__init__(None)
        self.constants = constants
        self.activated = False
        self.server_address = None
            
    def create_socket(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        self.server_address = (self.constants.ADDRESS, self.constants.PORT)
        self.log_emitter.emit(' starting up on %s port %s' % self.server_address)
        try:
            self.sock.bind(self.server_address)
            self.activated = True
        except socket.gaierror:
            self.log_emitter.emit('[Errno -2] Unknown name or service')
        finally:
            self.log_emitter.emit('DONE!')
            return self.activated

        
    
    def run(self):
        # Listen for incoming connections
        self.log_emitter.emit('Socket is listening!')
        self.sock.listen(1)
        while self.activated:
            self.log_emitter.emit('Waiting for a connection')
            try:
                self.connection, client_address = self.sock.accept()
                self.log_emitter.emit('Connection accepted from %s port %s ' % client_address)
            except:
                self.log_emitter.emit('Cannot accept connection due to a closed socket state.')
                break
            try:
                # Receive the data in small chunks and retransmit it
                while True:
                    data = self.connection.recv(128)

                    if data != b'':
                        self.socket_emitter.emit(data.decode())
                    # INCOMMING DATA
                    if data:
                        self.log_emitter.emit('Received "%s"' % data)
                       
                    else:
                        self.log_emitter.emit('No more data from ' + client_address)
                        break
            except:
                self.log_emitter.emit('Error while listening')
            finally:
                self.close_socket()
        
    def close_socket(self):  
        self.activated = False
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.log_emitter.emit('Socket is closed!')
        
        
