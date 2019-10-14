"""leg_model.py: Create the agent of model of the leg and provide an easy interface to be used with RL algorithms"""
__author__ = "Hany Hamed"
__credits__ = ["Hany Hamed", "Roman Fedorenko"]
__version__ = "0.0.1"
__email__ = "h.hamed.elanwar@gmail.com / h.hamed@innopolis.university"
__status__ = "Production"


import socket
import sys
import signal
import json
from time import *
import os
import random
import numpy as np
from transforms3d.euler import euler2mat

sim_exec = '/home/hany/repos/Work/IU/Tensegrity/Tensegrity-Robotics/src/dev/legz/python_communication_test/helper.sh'


class LegModel():
    def __init__(self, host_name='localhost', port_num=10008, packet_size=500, sim_exec=sim_exec):
        self.host_name = host_name
        self.port_num = port_num
        self.packet_size = packet_size
        self.sim_exec = sim_exec
        self.json_obj = {
            'Controllers_val': [0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0],
            'Reset': 0
        }
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create a TCP/IP socket
        self.server_address = (self.host_name, self.port_num) # Bind the socket to the port

        self.connection = None
        self.client_address = None
        print('#########\nstarting up on {} port {}\n#########'.format(self.server_address, self.port_num))
        self.sock.bind(self.server_address)
        self.sock.listen(1)  # Listen for incoming connections

    # function for writing data into TCP connection
    def write(self, data):
        # print('sending data to the client:"{}"'.format(data))
        try:
            self.connection.sendall(data.encode())
        except Exception as e:
            print("$$$$$$$$$$$$ ERROR in Writing $$$$$$$$$$$$")
            print("Error: " + str(e))

    # function for reading data from TCP connection
    def read(self):
        try:
            data = []
            counter = 1
            # Receive the data in small chunks and retransmit it
            while True:
                data.append(self.connection.recv(self.packet_size).decode("utf-8"))         #reading part
                # print('{} received "{}"'.format(counter,data[-1]))
                # print(data[-1][-14:-1], ('ZFinished' in str(data[-1][-14:-1])))
                if 'ZFinished' in str(data[-1][-14:-1]):
                    # print("FINISHED*************")
                    # sleep(5)
                    break
                counter += 1
            return "".join(data)
        except ValueError:
            print(ValueError)
            print("$$$$$$$$$$$$ ERROR in Reading $$$$$$$$$$$$")
            # sleep(2)
            return None

    def startSimulator(self):
        if(self.sim_exec == sim_exec):
            print("#Warning: Starting an old version")
        os.system(self.sim_exec)
        print('#########\nwaiting for a connection\n#########')
        self.connection, self.clientAddress = self.sock.accept()  #wait until it get a client
        print('connection from', self.clientAddress)

    def closeSimulator(self):
        pass
    
    def render(self):
        pass
    
    def reset(self):
        self.closeSimulator()
        # sleep(2)
        self.startSimulator()

def main():
    pass


if __name__ == "__main__":
    main()
