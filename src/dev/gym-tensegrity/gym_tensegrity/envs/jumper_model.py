"""Jumper_model.py: Create the agent of model of the Jumper and provide an easy interface to be used with RL algorithms"""
__author__ = "Hany Hamed"
__credits__ = ["Hany Hamed", "Prof. Sergie Savin"]
__version__ = "1.0.0"
__email__ = "h.hamed.elanwar@gmail.com / h.hamed@innopolis.university"
__status__ = "Testing"


import socket
import sys
import signal
import json
from time import *
import os
import subprocess
import random
import numpy as np
from transforms3d.euler import euler2mat

sim_exec = '/home/hany/repos/Work/IU/Tensegrity/Tensegrity-Robotics/src/dev/jumper/util/helper.sh'

class JumperModel():
    def __init__(self, host_name='localhost', port_num=10040, packet_size=5000,
                 sim_exec=sim_exec, dl=0.1, rods_num=19, controllers_num=60,
                 end_effector_index=4):
        self.host_name = host_name
        self.port_num = port_num
        self.packet_size = packet_size
        self.sim_exec = sim_exec
        self.actions_json = {
            'Controllers_val': [0,0,0,0,0,0,0,0],
            'Reset': 0
        }
        self.sim_json = {"Cables_lengths":
                        [0,0,0,0,0,0,0,0],
                         "End_points":
                        [[0.,0.,0.], [0.,0.,0.], [0.,0.,0.], [0.,0.,0.], 
                         [0.,0.,0.],[0.,0.,0.]],
                        "Time": 0.,
                        "ZFinished": 1,
                        "Flags":[1,0,0]}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print(self.port_num)
        self.server_address = (self.host_name, self.port_num) # Bind the socket to the port

        self.connection = None
        self.client_address = None
        self.child_process = None
        print('#########\nstarting up on {} port {}\n#########'.format(self.server_address, self.port_num))
        # print(self.server_address)
        self.sock.bind(self.server_address)
        self.sock.listen(1)  # Listen for incoming connections
        self.reset_flag = False
        self.close_flag = False
        self.dl = dl                            # Self modified parameter
        self.rods_num = rods_num                  # Self modified parameter
        self.controllers_num = controllers_num    # Self modified parameter
        self.end_effector_index = end_effector_index    # Self modified parameter

    def __del__(self):
        self.closeSimulator()
        # sys.exit(0)

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
                print('{} received "{}"'.format(counter,data[-1]))
                if 'ZFinished' in str(data[-1][-14:-1]):
                    break
                counter += 1
            return "".join(data)
        except ValueError:
            print(ValueError)
            print("$$$$$$$$$$$$ ERROR in Reading $$$$$$$$$$$$")
            # sleep(2)
            return None

    def startSimulator(self):
        self.close_flag = False
        self.reset_flag = False
        if(self.sim_exec == sim_exec):
            print("#Warning: Starting an old version")
        # sleep(0.5)
        self.child_process = subprocess.Popen(self.sim_exec)
        print('#########\nwaiting for a connection\n#########')
        self.connection, self.clientAddress = self.sock.accept()  #wait until it get a client
        print('connection from', self.clientAddress)

    def closeSimulator(self):
        self.close_flag = True
        # kill the shell script of the simulator
        if self.connection is not None:
            self.connection.close()
        if self.child_process is not None:
            os.kill(self.child_process.pid, signal.SIGKILL)

    def render(self):
        pass
    
    def reset(self):
        self.reset_flag = True
        self.closeSimulator()
        # os.kill(self.child_process.pid, signal.SIGTERM)
        # sleep(1)
        self.startSimulator()

    def step(self):
        if (self.close_flag == False):
            if (self.reset_flag == True):
                self.reset()
            
            self.write(json.dumps(self.actions_json))   # Write to the simulator module the json object with the required info

            sim_raw_data = self.read()
            # print(sim_raw_data)
            if(sim_raw_data is not None):
                self.sim_json = json.loads(sim_raw_data)  # Parse the data from string to json
        else:
            self.closeSimulator()

    def getCablesLengths(self, i=None):
        if(i is None):
            return self.sim_json["Cables_lengths"]
        return self.sim_json["Cables_lengths"][i]
        
    def _getEndPointsByRod(self, rod_num):
        end_point1 = self.sim_json["End_points"][rod_num][0]
        end_point2 = self.sim_json["End_points"][rod_num][1]
        return [[end_point1[0],end_point1[1],end_point1[2]], [end_point2[0],end_point2[1],end_point2[2]]]
    
    def getEndPoints(self, rod_num=None):
        if(rod_num is None):
            # [rod1, rod2,...] -> [endPoint1, endPoint2] -> [x,y,z]
            end_points = []
            for i in range(self.rods_num):
                end_points.append(self._getEndPointsByRod(i))
            return end_points
        return self._getEndPointsByRod(rod_num)

   # TODO
    def getLegAngle(self):
        pass    
    
    def getTime(self):
        return self.sim_json["Time"]

# This function for testing the model by itself
def main():
    jumper = JumperModel()
    jumper.actions_json["Controllers_val"][2] = 0
    jumper.actions_json["Controllers_val"][5] = 0
    def cleanExit(signal, frame):
        print("HANDLER")
        jumper.__del__()
        exit()
    # signal.signal(signal.SIGTERM, cleanExit) 
    signal.signal(signal.SIGINT, cleanExit) # Activate the listen to the Ctrl+C

    jumper.startSimulator()
    sleep(1)
    jumper.reset()
    # sleep(3)
    # jumper.reset()
    sleep(1)
    jumper.closeSimulator()
    sleep(5)

    # start_time = time()
    # print(start_time)
    # reset = False
    # # input()   
    # while(True):
    #     jumper.step()
    #     # input("input now")
    #     # sleep(0.01)
    #     if(time() - start_time > 20):
    #         # jumper.closeSimulator()
    #         pass    
    #         # jumper.close_flag = True
    #     if( time() - start_time > 5 and reset == False):
    #         reset = True
    #         # jumper.reset()
    #         # jumper.reset_flag = True





if __name__ == "__main__":

    main()

