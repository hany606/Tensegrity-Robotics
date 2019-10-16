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
import subprocess
import random
import numpy as np
from transforms3d.euler import euler2mat

sim_exec = '/home/hany/repos/Work/IU/Tensegrity/Tensegrity-Robotics/src/dev/legz/python_communication_test/helper.sh'


class LegModel():
    def __init__(self, host_name='localhost', port_num=10013, packet_size=5000,
                 sim_exec=sim_exec, dl=0.1, rods_num=19, controllers_num=60,
                 end_effector_index=4):
        self.host_name = host_name
        self.port_num = port_num
        self.packet_size = packet_size
        self.sim_exec = sim_exec
        self.actions_json = {
            'Controllers_val': [0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0],
            'Reset': 0
        }
        self.sim_json = {"Flags":[1,0,0]}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create a TCP/IP socket
        self.server_address = (self.host_name, self.port_num) # Bind the socket to the port

        self.connection = None
        self.client_address = None
        print('#########\nstarting up on {} port {}\n#########'.format(self.server_address, self.port_num))
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
        sys.exit(0)

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
        os.kill(self.child_process.pid, signal.SIGTERM)

    def render(self):
        pass
    
    def reset(self):
        self.reset_flag = True
        self.closeSimulator()
        # sleep(2)
        self.startSimulator()

    # TODO: make a general step function
    def step(self):
        if (self.close_flag == False):
            if (self.reset_flag == True):
                self.reset()
            
            # if(self.sim_json["Flags"][0] == 1):
            #     self.actions_json["Controllers_val"][2] = -1*self.actions_json["Controllers_val"][2]
            #     self.actions_json["Controllers_val"][5] = -1*self.actions_json["Controllers_val"][5]
                
                # print("FLIP")
                # input()            
            print("write")
            self.write(json.dumps(self.actions_json))   # Write to the simulator module the json object with the required info

            sim_raw_data = self.read()
            # print(sim_raw_data)
            if(sim_raw_data is not None):
                self.sim_json = json.loads(sim_raw_data)  # Parse the data from string to json
            # print(self.sim_json["Center_of_Mass"][4])
            # print("step Function",self.sim_json["Cables_lengths"][2])

        else:
            self.closeSimulator()

    def getCablesLengths(self, i=None):
        # print("getCableLengths Function",self.sim_json["Cables_lengths"][2])
        if(i is None):
            return self.sim_json["Cables_lengths"]
        return self.sim_json["Cables_lengths"][i]
        
    #TODO
    def _getEndPointsByRod(self, rod_num):
        # print(self.sim_json["Center_of_Mass"][0])
        # print(rod_num, type(rod_num))
        rods_cms = self.sim_json["Center_of_Mass"][rod_num]
        rods_orientation = self.sim_json["Orientation"][rod_num]
        # ....
        # ....
        # ....
        # [endPoint1, endPoint2] -> [x,y,z]
        return [[0,0,0], [0,0,0]]

    def getEndPoints(self, rod_num=None):
        if(rod_num is None):
            # [rod1, rod2,...] -> [endPoint1, endPoint2] -> [x,y,z]
            end_points = []
            for i in range(self.rods_num):
                end_points.append(self._getEndPointsByRod(i))
            return end_points
        return self._getEndPointsByRod(rod_num)

    def getEndEffector(self):
        return self._getEndPointsByRod(self.end_effector_index)[0]

        
    
    def getTime(self):
        return self.sim_json["Time"]

# This function for testing the model by itself
def main():
    leg = LegModel()
    leg.actions_json["Controllers_val"][2] = 5
    leg.actions_json["Controllers_val"][5] = 5
    def cleanExit(signal, frame):
        print("HANDLER")
        leg.__del__()
    # signal.signal(signal.SIGTERM, cleanExit) 
    signal.signal(signal.SIGINT, cleanExit) # Activate the listen to the Ctrl+C

    leg.startSimulator()
    # sleep(5)
    # leg.closeSimulator()

    start_time = time()
    reset = False
    while(True):
        leg.step()
        if(time() - start_time > 20):
            # leg.closeSimulator()
            pass    
            # leg.close_flag = True
        if( time() - start_time > 5 and reset == False):
            reset = True
            # leg.reset()
            # leg.reset_flag = True





if __name__ == "__main__":

    main()

