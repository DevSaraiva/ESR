import socket
import threading
from threading import Thread
import json
import sys
import pickle
import ServerWorker

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



    
def initializeConnections(topo):
    
    print('Inicializing Connections')
    # get the hostname
    port = 1234
    #read config file
    dicTopo = readConfigFile(topo)
    nodesNumber = len(dicTopo)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))  
    server_socket.listen(nodesNumber) 
    for i in range(nodesNumber):
        conn, address = server_socket.accept()  # accept new connection
        data = conn.recv(1024).decode()
        if not data:
            break
        neighboursList = []
        #getting neighbours list
        for key,value in dicTopo.items():
            
            if address[0] in value['names']:
                print('sendig neighbours to ' + key)
                neighboursList = value['neighbours']
        conn.send(pickle.dumps(neighboursList))  # send data to the client
    conn.close()  # close the connection



if __name__ == '__main__':

    topo = sys.argv[1]

    Thread(target=initializeConnections, args = (topo,)).start()
    Thread(target=server, args = ()).start()


    