import socket
import threading
from threading import Thread
import json
import sys
import pickle
import ServerWorker
import b_database
from time import sleep


def readConfigFile(topo):
    print('reading config file ..')
    with open(topo) as json_file:
        data = json.load(json_file)
    return data


def server():
	try:
		SERVER_PORT = 5555
	except:
		print("[Usage: Server.py Server_port]\n")
	rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	rtspSocket.bind(('', SERVER_PORT))
	rtspSocket.listen(5)    
	# Receive client info (address,port) through RTSP/TCP session
	while True:
		clientInfo = {}
		clientInfo['rtspSocket'] = rtspSocket.accept()
		ServerWorker(clientInfo).run()		


def initializeConnectionsWorker(conn,address,dicTopo,database):
    
        database.addPeerConnected()
        data = conn.recv(1024).decode()
        if data:
            neighboursList = []
            #getting neighbours list
            for key,value in dicTopo.items():
            
                if address[0] in value['names']:
                    print('sendig neighbours to ' + key)
                    neighboursList = value['neighbours']

            while(b_database.getPeersConnected() < 2):
                print('Not enough peers')
                sleep(2)
    
        conn.send(pickle.dumps(neighboursList))  # send data to the client
        conn.close()  # close the connection


    
def initializeConnections(topo, database):
    
    print('Inicializing Connections')
    # get the hostname
    port = 1111
    #read config file
    dicTopo = readConfigFile(topo)
    nodesNumber = len(dicTopo)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))  
    server_socket.listen(nodesNumber) 
    for i in range(nodesNumber):
        conn, address = server_socket.accept()  # accept new connection
        Thread(target=initializeConnectionsWorker, args = (conn,address,dicTopo,database)).start()
    



if __name__ == '__main__':

    b_database = b_database.b_database()
    topo = sys.argv[1]

    Thread(target=initializeConnections, args = (topo,b_database)).start()
    Thread(target=server, args = ()).start()


    