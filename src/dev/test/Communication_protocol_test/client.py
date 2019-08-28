#Reference: https://pymotw.com/2/socket/tcp.html

import socket
import sys
import time

packet_size = 100
port_num = 10006
hostname = 'localhost'


def write(sock, data):
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(data)

def read(sock):
    data = []
    data.append(sock.recv(packet_size))
    print >>sys.stderr, 'received "%s"' % data[-1]
    # amount_received = 0
    # amount_expected = max_data_size
    
    # while amount_received < amount_expected:
    #     data.append(sock.recv(packet_size))
    #     amount_received += len(data[-1])
    #     if(len(data[-1]) == 0):
    #         break
    #     print >>sys.stderr, 'received "%s"' % data[-1]
    return "".join(data)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (hostname, port_num)
print >>sys.stderr, '#########\nconnecting to %s port %s\n#########' % server_address
message = 'Hello from the client'


sock.connect(server_address)
while True:
    try:
        # Send data
        print("write-----------------------------")
        write(sock, message) #writing part
        print("read-----------------------------")
        print(read(sock))
    finally:
        print >>sys.stderr, 'closing socket'
        time.sleep(1)
sock.close()
