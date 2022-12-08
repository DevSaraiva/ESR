import socket
from threading import Thread
import json
import sys
import pickle
import b_database
from time import sleep
import time


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

            while(database.getPeersConnected() < len(database.getTopo().keys()) - 1):
                sleep(1)
    
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


            

    
    
   





if __name__ == '__main__':

    database = b_database.b_database()
    database.setTopo(readConfigFile(sys.argv[1]))

    Thread(target=initializeConnections, args = (database,)).start()
    Thread(target=sendStatusServerNetwork, args = (database,)).start()


    