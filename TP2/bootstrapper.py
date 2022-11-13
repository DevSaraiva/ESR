import socket
import threading
import json
import sys
import pickle

def readConfigFile(topo):
    print('reading config file ..')
    with open(topo) as json_file:
        data = json.load(json_file)
    return data


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
        
        if self.wait : data = client_socket.recv(1024).decode()  # receive response

        print('Response from peer ' + self.hostToConnect + ' : ' + data)

        client_socket.close()  # close the connection




class server(threading.Thread):
    def __init__(self,topo):
        threading.Thread.__init__(self)
        self.topo = topo
        
    # helper function to execute the requests
    def run(self):

        print('server staring')
        # get the hostname
        port = 1234

        #read config file
        dicTopo = readConfigFile(self.topo)
        nodesNumber = len(dicTopo)

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
        server_socket.bind(('', port))  # bind host address and port together 
        server_socket.listen(nodesNumber) # configures how many client the server can listen simultaneously

        for i in range(nodesNumber):

            print('new connection')

            conn, address = server_socket.accept()  # accept new connection

            print('accepted')

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

    server = server(topo)
    server.start()

    