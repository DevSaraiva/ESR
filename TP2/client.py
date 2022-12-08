import socket
import threading
import pickle
import sys
import database
from threading import Thread
from time import time
from time import sleep
from Cliente import Client
from tkinter import Tk

def send(host_to_connect,port):
        print(host_to_connect)
        client_socket = socket.socket()  # instantiate
        client_socket.connect((host_to_connect, 2555 ))  # connect to the server
        client_socket.send(port.encode())
        
        root = Tk()
        # Create a new client
        app = Client(root, host_to_connect, port, '5008', 'movie.Mjpeg')
        app.master.title("RTPClient")	
        root.mainloop()



if __name__ == '__main__':
        host_to_connect = sys.argv[1]
        port = sys.argv[2]
        Thread(target=send, args = (host_to_connect,port)).start()