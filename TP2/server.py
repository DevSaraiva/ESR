import socket
from threading import Thread
import json
import sys
import pickle
import b_database
from time import sleep
import time
import os
import re


def readConfigFile(topo):
    print('reading config file ..')
    with open(topo) as json_file:
        data = json.load(json_file)
    return data


def initializeConnectionsWorker(conn,address,database):
    
        database.addPeerConnected()
        data = conn.recv(1024).decode()
        if data:
            neighboursList = []
            #getting neighbours list
            for key,value in database.getTopo().items():
            
                if address[0] in value['names']:
                    print('sendig neighbours to ' + key)
                    neighboursList = value['neighbours']

            while(database.getPeersConnected() < database.getNumberPeer()):
                pass
    
        conn.send(pickle.dumps(neighboursList))  # send data to the client
        conn.close()  # close the connection


def initializeConnections(database):
    
    print('Inicializing Connections')
    # get the hostname
    port = 1111
    #read config file
    nodesNumber = len(database.getTopo().keys()) - 1
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))  
    server_socket.listen(nodesNumber) 
    for i in range(nodesNumber):
        conn, address = server_socket.accept()  # accept new connection
        Thread(target=initializeConnectionsWorker, args = (conn,address,database)).start()
    

def sendStatusServerNetwork(database):
    
    status_socket = socket.socket()  # instantiate
    myname = socket.gethostname()
    neighbours = database.getTopo()[myname]['neighbours']
    while True:

        for neighbour in neighbours:
            connected = False
            while connected == False: 
                try:
                    status_socket.connect((neighbour, 4444))  # connect to the server
                    message = f'servername:{myname} time:{time.time()} jumps:{0} visited:'
                    status_socket.send(message.encode())  # send message
                    connected = True
                    print('connected')
                    
                except:
                    pass
        sleep(15)


            
def readVideoFile(filename, b_database):
    print("Reading Video File and saving to database...")
    try:
        file = open(filename, 'rb')
    except:
        print("Error opening file!")
        raise IOError
    frameNum = 0
    buffer = []
    ###### Get next frame (nextFrame from VideoStream.py)
    file_stats = os.stat(filename)
    unread_FileSize_bytes = file_stats.st_size  #here it represents the total size of the file in bytes, because none was read untill now
    print(f'File Size in Bytes is {unread_FileSize_bytes}')
    while (unread_FileSize_bytes ) > 0:
        data = file.read(5) # Get the framelength from the first 5 bytes
        if data:
            frameLenght = int(data)
            #Read the current frame
            data = file.read(frameLenght)
            buffer.append(data)
            frameNum += 1 
        unread_FileSize_bytes = unread_FileSize_bytes - 5 - frameLenght
    
    
    b_database.setFile(buffer)  
    


def receiveStreamRequest(database):

        udpSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udpSocket.bind(('', 6666))

        while(True):

                msg , address = udpSocket.recvfrom(1024)

                request = msg.decode()

                splitted = re.split(' ',request)

                filename = splitted[0]

                readVideoFile(filename, database)
                
                file = database.getFile()
                
                i = 0
                while True:
                    for frame in file:
                        print(i)
                        sleep(0.0005)
                        udpSocket.sendto(frame, address)
                        i += 1

                   

if __name__ == '__main__':

    database = b_database.b_database()
    database.setTopo(readConfigFile(sys.argv[1]))
    option = int(sys.argv[2])

    if(option==1):
        Thread(target=initializeConnections, args = (database,)).start()
    Thread(target=sendStatusServerNetwork, args = (database,)).start()
    Thread(target=receiveStreamRequest, args = (database,)).start()
    