import socket
import threading
import pickle
import sys
import database
from threading import Thread


#Inizialize the connection with the server to get neighbours list

    
def connectionRequest(port_to_connect,host_to_connect,message,database):

        print('Requesting Neighbours...')
        client_socket = socket.socket()  # instantiate
        client_socket.connect((host_to_connect, port_to_connect))  # connect to the server
        client_socket.send(message.encode())  # send message
    
        data = client_socket.recv(1024)  # receive response

        client_socket.close()  # close the connection

        database.putNeighbours(pickle.loads(data))
        

if __name__ == '__main__':

    database = database.database()
    bootstrapper = sys.argv[1]
    Thread(target=connectionRequest, args = (1234,bootstrapper,'NEEDS THE NEIGHBOURS LIST',database)).start()
   






    