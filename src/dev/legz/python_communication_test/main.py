##################################################################################################
# About: Server TCP code, get json object from the simulator and send another json object and
#       process the data using stable baseline
# Notes:
#TODO (DONE): Adapt this on python3 to solve the issues in json parser in python3
#there is difference in json.loads as it only accept string not bytes  and in 3 TCP read return bytes
#and str not converting from bytes to str in py3 but .decode('UTF-8') does
#and the same for sendall function of TCP it only takes bytes so we need to encode the string first to bytes like object
#and solving some errors like https://bugs.python.org/issue24283

#Reference: https://pymotw.com/2/socket/tcp.html

#Coding Style: camelCase
# Run it with . ~/virtualenvs/baselines_env/bin/activate

##################################################################################################
#import the libraries
import socket
import sys
import signal
import json
from time import sleep
import os

# import stable_baselines

print("Finish importing the libraries")

#import openai
#import tensorflow as tf
#import numpy as np
#from baselines import ...

#--------------------------------------------Vars--------------------------------------------

#Settings for the TCP communication
packetSize = 500
portNum = 10023
hostName = 'localhost'
# connection = None
# clientAddress = None

globalFlag = 0  #this is used to reset the NTRT environment and TCP connection with it

# JSON object structure
jsonObj = {
    'Controllers': [0,0,0,0,0,0],
    'Reset': 0
}
#--------------------------------------------------------------------------------------------


#--------------------------------------------Functions--------------------------------------------
# Ctrl+C Handle to close safely the TCP connection
def signalHandler(signal, frame):
    # print('You pressed Ctrl+C!')
    tmp = str(input("You want reset or close: r/c: \n"))
    print(tmp)
    if(tmp == 'r'):
        reset()
    elif(tmp == 'c'):
        print("----------------------------------Exit-----------------------------------")
        global globalFlag
        globalFlag = 2
    else:
        # print("Please  Ctrl+C and write 'r' or 'c' ")
        sleep(5)
# function for writing data into TCP connection
def write(connection, data):
    print('sending data to the client:"{}"'.format(data))
    try:
        connection.sendall(data.encode())
    except Exception as e:
        print("$$$$$$$$$$$$ ERROR in Writing $$$$$$$$$$$$")
        print("Error: " + str(e))

# function for reading data from TCP connection
def read(connection):
    try:
        data = []
        # Receive the data in small chunks and retransmit it
        # while True:
        data.append(connection.recv(packetSize))         #reading part
        print('received "{}"'.format(data[-1]))
            # if not(data[-1]):
            #     print >>sys.stderr, 'no more data from', client_address
            #     break
        return data[-1]
    except:
        print("$$$$$$$$$$$$ ERROR in Reading $$$$$$$$$$$$")
        return None
def reset():
    global globalFlag
    globalFlag = 1

def main():
    while True:
        #Note: TODO: Make in the simulator wait a second then send a message
        os.system('/home/hany/repos/Work/IU/Tensegrity/Tensegrity-Robotics/src/dev/legz/python_communication_test/helper.sh')

        print('#########\nwaiting for a connection\n#########')
        connection, clientAddress = sock.accept()  #wait until it get a client
        print('connection from', clientAddress)
        global globalFlag
        globalFlag = 0
        while True:
            r = read(connection)
            if(r != None):
                jsonObjTmp = json.loads(r.decode("utf-8"))  # Parse the data from string to json
            # TODO: Use the incoming data after being converted to json

            # TODO:
            # Take the data from the simulator module
            # Formulate the data as observation
            # Generate Reward
            # Feed the RL Algorithm with Reward and observartion
            # Generate Action
            # Decide either end of episode (Reset the simulator) or specific Action
            # Modify the action in json

            write(connection,json.dumps(jsonObj))   # Write to the simulator module the json object with the required info
            if(globalFlag > 0):
                print("GLOBAL FLAG Exit")
                break
        connection.close()
        if(globalFlag == 2):
            sys.exit(0)
#-------------------------------------------------------------------------------------------------


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create a TCP/IP socket
serverAddress = (hostName, portNum) # Bind the socket to the port


print('#########\nstarting up on {} port {}\n#########'.format(serverAddress, portNum))
sock.bind(serverAddress)
sock.listen(1)  # Listen for incoming connections



signal.signal(signal.SIGINT, signalHandler) # Activate the listen to the Ctrl+C

# This is top open the simulator
print("Opening the NTRT simulator")

main()