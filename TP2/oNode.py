import socket
import pickle
import sys
import database
from threading import Thread
import time
from time import sleep
import re
import netifaces


#Inizialize the connection with the server to get neighbours list

    
def neighboursRequest(host_to_connect,database):

        port_to_connect = 1111
        print('Requesting Neighbours...')
        client_socket = socket.socket()  # instantiate
        client_socket.connect((host_to_connect, port_to_connect))  # connect to the server
        message = "REQ_NEIGHBOURS"
        client_socket.send(message.encode())  # send message
    
        data = client_socket.recv(1024)  # receive response

        client_socket.close()  # close the connection


        neighboursParsed = []

        serversNeighboursParsed = []

        neighboursUnParsed = pickle.loads(data)

        for neighbour in neighboursUnParsed:
                if 's' not in neighbour:
                        neighboursParsed.append(neighbour)
                else:
                        
                        serversNeighboursParsed.append(neighbour.replace('s', ''))


        database.putNeighbours(neighboursParsed)
        database.putServersNeighbours(serversNeighboursParsed)

        print(neighboursParsed)
        print(serversNeighboursParsed)


        Thread(target=receiveStatusServerNetwork, args = (database,)).start()

# Initialize connection with neighbours

def sendMessage(database):

        for neighbour in database.getNeighbours():
                neighbour_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                while database.getConnection(neighbour) == False:
                        try:
                                neighbour_socket.connect((neighbour, 9999))

                                data = neighbour_socket.recv(1024)  # receive response

                                response = data.decode

                                if(response == 'ACK'):
                                        database.putConnection(neighbour,neighbour_socket)
                                else:
                                        break

                        except:
                                print('cant establish')
                                pass
                
                

# Listen connections 

def listenNodesConnections(database):

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', 9999))  
        server_socket.listen(10)
        
        for neighbour in database.getNeighbours():
                print('listenning')
                conn, address = server_socket.accept()  # accept new connection
                data = conn.recv(1024).decode()
                print(data, 'from ' + address[0])
                

def receiveStatusServerNetwork(database):

        print('receiving status',flush=True)
        status_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        status_socket.bind(('', 4444))  
        status_socket.listen(10)

        while True:
                conn, address = status_socket.accept()

                # print('received from ',address[0],flush=True)
                data = conn.recv(1024)
                # print(data.decode(),flush=True)

                msg = data.decode()

                splitted = re.split(' ',msg)

                connection = {}
                
                timeserver = 0
                for string in splitted:
                    s = re.split(r':',string)
                    if s[0] == 'servername':
                        servername = s[1]
                        connection['servername'] = servername
                    if s[0] == 'time':
                        timeserver += float(s[1])
                        timestamp = time.time() - float(s[1])
                        connection['timestamp'] = timestamp
                    if s[0] == 'jumps':
                        jumps = int(s[1])
                        connection['jumps'] = jumps
                    if s[0] == 'visited':
                        visited = re.split(',',s[1])
                        if '' in visited : visited.remove('')
                        connection['visited'] = visited
                
                #get my names
                mynames = []
                index = 0
                for interface in netifaces.interfaces():
                        if(index != 0):
                                for link in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                                        mynames.append(link['addr'])
                        index = index + 1

                #construct visited list with all node names
                visited = ""
                index = 0
                if len(connection['visited']) != 0:
                        for vis in connection['visited']:
                                if(index == 0):
                                        visited = visited + vis
                                else:
                                        visited = visited + ',' + vis
                                index = index + 1
                        for name in mynames:
                                visited = visited + ',' + name
                                
                else:
                        for name in mynames:
                                if index == 0 :visited = visited + name
                                else: visited = visited + ',' + name
                                index = index + 1
                                

                database.putConnectionServerStatus(address[0],connection)
                
                print(database.getConnectionServerStatus(address[0]))
                message = f'servername:{connection["servername"]} time:{timeserver} jumps:{connection["jumps"] + 1} visited:{visited}'

                for neighbour in database.getNeighbours():
                        if(neighbour not in connection['visited']):
                                connected = False
                                while connected == False: 
                                    try:
                                        status_socket_send = socket.socket()
                                        status_socket_send.connect((neighbour,4444))
                                        status_socket_send.send(message.encode())
                                        status_socket_send.close()
                                        connected = True
                                    except:
                                        pass
                                        



if __name__ == '__main__':

        database = database.database()
        bootstrapper = sys.argv[1]
        Thread(target=neighboursRequest, args = (bootstrapper,database)).start()
        
       
        
        
   






    