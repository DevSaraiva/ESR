import socket
import threading
import time

class server(threading.Thread):
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
 
    # helper function to execute the requests
    def run(self):

        print('server staring')
        # get the hostname
        host = socket.gethostname()
        port = 5000 

        server_socket = socket.socket()  # get instance
        server_socket.bind((host, port))  # bind host address and port together

        server_socket.listen(2) # configures how many client the server can listen simultaneously
        
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            if not data:
                break
            print("from connected user: " + str(data))
            data = input(' -> ')
            conn.send(data.encode())  # send data to the client

        conn.close()  # close the connection

class client(threading.Thread):
    def __init__(self, thread_name, thread_ID,host_to_connect,port_to_connect):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.hostToConnect = host_to_connect
        self.portToConnect = port_to_connect
 
    
    def run(self):

        print('client staring')
        client_socket = socket.socket()  # instantiate
        client_socket.connect((self.hostToConnect, self.portToConnect))  # connect to the server

        message = input(" -> ")  # take input

        while message.lower().strip() != 'bye':
            client_socket.send(message.encode())  # send message
            data = client_socket.recv(1024).decode()  # receive response

            print('Received from server: ' + data)  # show in terminal

            message = input(" -> ")  # again take input

        client_socket.close()  # close the connection




if __name__ == '__main__':
    server = server("server", 1000)
    client = client("client", 2000,socket.gethostname(),5000)

    server.start()

    time.sleep(1)

    client.start()
    