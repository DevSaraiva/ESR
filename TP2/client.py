import socket
import sys
from threading import Thread
from Cliente import Client
from tkinter import Tk

def send(host_to_connect,filename):
        print(host_to_connect)
        client_socket = socket.socket()  # instantiate
        client_socket.connect((host_to_connect, 2555 ))  # connect to the server
        client_socket.send(filename.encode())
        
        root = Tk()
        # Create a new client
        app = Client(root, host_to_connect, 7777, '5008', filename)
        app.master.title("RTPClient")	
        root.mainloop()



if __name__ == '__main__':
        host_to_connect = sys.argv[1]
        filename = sys.argv[2]
        Thread(target=send, args = (host_to_connect,filename)).start()