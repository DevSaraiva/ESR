import socket
import threading
import pickle
import sys

class server(threading.Thread):
    def __init__(self,bootstrapper):
        threading.Thread.__init__(self)
        self.bootstrapper = bootstrapper

 
    # helper function to execute the requests
    def run(self):

        #get neighbours list

        neighboursList = messageSender(1234,self.bootstrapper,'NEEDS THE NEIGHBOURS LIST',True)

        print('peer staring')
        port = 1234 

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
        server_socket.bind(('0.0.0.0', port))  # bind host address and port together

        server_socket.listen(5) # configures how many client the server can listen simultaneously
        
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024)
            if not data:
                break
            print("from connected user: " + pickle.loads(data))
            

        conn.close()  # close the connection

class messageSender(threading.Thread):
    def __init__(self,port_to_connect,host_to_connect,message,wait):
        threading.Thread.__init__(self)
        self.portToConnect = port_to_connect
        self.hostToConnect = host_to_connect
        self.message = message
        self.wait = wait
 
    
    def run(self):

        print('sending message')
        client_socket = socket.socket()  # instantiate
        client_socket.connect((self.hostToConnect, self.portToConnect))  # connect to the server
        client_socket.send(self.message.encode())  # send message
        
        data = ''

        if self.wait : 
            data = client_socket.recv(1024)  # receive response
            print('Response from peer ' + self.hostToConnect + ' : ' + str(pickle.loads(data)))

        client_socket.close()  # close the connection

        return data

        




if __name__ == '__main__':

    bootstrapper = sys.argv[1]

    server = server(bootstrapper)

    server.start()




    