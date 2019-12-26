"""Jumper_model.py: Create the agent of model of the one legged jumping tensegrity robot and provide an easy interface to be used with RL algorithms"""
__author__ = "Hany Hamed"
__credits__ = ["Hany Hamed", "Vlad Kurenkov", "Prof. Sergie Savin", "Oleg Balakhnov"]
__version__ = "1.0.0"
__email__ = "h.hamed.elanwar@gmail.com / h.hamed@innopolis.university"
__status__ = "Developing"


import socket
import sys
import signal
import json
from time import *
import os
import subprocess
import numpy as np

path_to_model = os.path.join(os.environ["TENSEGRITY_HOME"], "build/dev/jumper/AppJumperModel")
sim_exec = "gnome-terminal -e {}".format(path_to_model)

class JumperModel():
    def __init__(self, host_name='localhost', port_num=10040, packet_size=5000,
                 sim_exec=sim_exec, dl=0.1, controllers_num=8):
        self.host_name = host_name
        self.port_num = port_num
        self.packet_size = packet_size
        self.sim_exec = sim_exec + ' {:} {:}'.format(host_name, port_num)
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
        self.end_points_num = 6
        self.controllers_num = controllers_num    # Self modified parameter
        self.leg_end_points = [4,5]
        self.leg_length = 20

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
                # print('{} received "{}"'.format(counter,data[-1]))
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
        # subprocess_args = [self.sim_exec[:14], self.sim_exec[15:]]
        #Machine with Xscreen
        subprocess_args = self.sim_exec.split(" ")
        subprocess_args[2] = " ".join(subprocess_args[2:])
        self.child_process = subprocess.Popen(subprocess_args[:3])  
        #Headless
        # self.child_process = subprocess.Popen(self.sim_exec, shell=True)  
        #print('#########\nwaiting for a connection\n#########')
        self.connection, self.clientAddress = self.sock.accept()  #wait until it get a client
        #print('connection from', self.clientAddress)

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
        
    def getEndPoints(self):
        end_points = []
        for i in range(self.end_points_num):
            end_points.append(self.sim_json["End_points"][i])
        return end_points

    # point_a: is the end point of the leg from down
    # point_b: is the end point of the virtual horizontal leg from up
    # point_c: is the end point of the actual leg from up
    def getLegAngle(self):
        point_a = np.array(self.sim_json["End_points"][self.leg_end_points[0]])
        point_b = [0,0,0]
        point_b[:] = point_a[:]
        point_b[1] += self.leg_length
        point_c = np.array(self.sim_json["End_points"][self.leg_end_points[1]])
        v1 = point_b - point_a
        v2 = point_c - point_a
        dot_product = np.dot(v1,v2)
        v1_mag = np.linalg.norm(v1)
        v2_mag = np.linalg.norm(v2)
        # print("pointa", point_a)
        # print("pointb",point_b)
        # print("pointc", point_c)
        # print("v1", v1)
        # print("v2", v2)
        # print("dot_product", dot_product)
        # print("1 mag", v1_mag)
        # print("2 mag", v2_mag)
        # print("arccos", np.arccos(dot_product/(v1_mag*v2_mag)))
        angle = np.arccos(dot_product/(v1_mag*v2_mag))
        # print("angle", angle)
        return angle
    
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

