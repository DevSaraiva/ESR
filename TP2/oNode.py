import socket
import threading
import pickle
import sys
import database
from threading import Thread
from time import time
from time import sleep


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

        database.putNeighbours(pickle.loads(data))

        print(database.getNeighbours())

# Initialize connection with neighbours

def initializeConnection(database):

        for neighbour in database.getNeighbours():
                print(neighbour)
                dict = {}
                neighbour_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                established = False
                while established is False:
                        try:
                                neighbour_socket.connect((neighbour, 5555))
                                established = True
                                
                        except:
                                print('cant establish')
                                sleep(1)
                                pass
                
                print('established')
                dict['neighbour_socket'] = neighbour_socket
                message = "HELLO"
                initialTime = time()
                neighbour_socket.send(message.encode())  # send message
                data = neighbour_socket.recv(1024)  # receive response
                endTime = time()
                delay = endTime - initialTime
                dict['delay'] = delay
                database.putConnection(neighbour,dict)
                print(data.decode())
                print(delay)


# Listen connections tries and keep alive packets

def listenConnections(database):

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', 5555))  
        server_socket.listen(10)
        
        while True:
                print('listenning')
                conn, address = server_socket.accept()  # accept new connection
                data = conn.recv(1024).decode()
                print(data, 'from ' + address[0])
                if(database.getConnection(address[0]) != False):
                        message = "ACK"
                        conn.send(message.encode())
                else:
                        print(database.getConnection(address[0]))
                        message = "NAK"
                        conn.send(message.encode())
                












if __name__ == '__main__':

        database = database.database()
        bootstrapper = sys.argv[1]
        Thread(target=neighboursRequest, args = (bootstrapper,database)).start()
        Thread(target=listenConnections, args = (database,)).start()
        Thread(target=initializeConnection, args = (database,)).start()
        
   






    