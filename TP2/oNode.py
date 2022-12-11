import socket
import pickle
import sys
import database
from threading import Thread
import time
from time import sleep
import re
import netifaces
import ServerWorker


def getMyNames():
        mynames = []
        index = 0
        for interface in netifaces.interfaces():
                if(index != 0):
                        for link in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                                    mynames.append(link['addr'])
                index = index + 1
        return mynames



def getStream(database,filename):
        #get best connection
        #só está a considerar o servidor

        print('getting stream')

        bestNeighbour = database.getBestMetricsServerStatus()

        database.putStreamEmpty(filename)

        #sending request
        msg       = f'{filename}'
        udpSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udpSocket.sendto(msg.encode(), (bestNeighbour,6666))
        
        i = 0
        while True:
                response,adress = udpSocket.recvfrom(100000)
                i = i +1
                print(i)
                database.putStreamPacket(filename,response)
        
        


def receiveStreamRequest(database):

        udpSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udpSocket.bind(('', 6666))

        while(True):

                msg , address = udpSocket.recvfrom(100000)

                filename = msg.decode()
                
                if database.getStream(filename) != False:
                        pass
                else:
                        Thread(target=getStream, args = (database,filename)).start()        
                        
               
                while database.getStreamState(filename) == False:
                        pass
                        
                while database.getStreamState(filename) == 'activated':
                        packet = database.popStreamPacket(filename)
                        if(packet != None):
                                udpSocket.sendto(packet,address)
                

# Sending a reply to client

def verifyStreamInNeighbourHood(database, filename,visited):
        
        mynames = getMyNames()
        newvisited = ""
        index = 0
        if len(visited) != 0:
                for vis in visited:
                        if(index == 0):
                                newvisited = newvisited + vis
                        else:
                                newvisited = newvisited + ',' + vis
                        index = index + 1
                for name in mynames:
                        newvisited = newvisited + ',' + name
                        
        else:
                for name in mynames:
                        if index == 0 :newvisited = newvisited + name
                        else: visited = newvisited + ',' + name
                        index = index + 1

        responses = []

        for neighbour in database.getNeighbours():
                if neighbour not in visited:
                        stream_socket = socket.socket()  # instantiate
                        stream_socket.connect((neighbour, 8888))  # connect to the server
                        message = f'filename:{filename} visited:{newvisited} '
                        stream_socket.send(message.encode())  # send message

                        response = stream_socket.recv(1024).decode()
                        print(response)

                        
                        if response != 'NAK':
                                responses.append(f'filename:{filename} neighbour:{neighbour} {response}')
                        
        
        return responses


def receiveStreamVerification(database):
        
        verification_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        verification_socket.bind(('', 8888))  
        verification_socket.listen(10)

        while True:
                conn, address = verification_socket.accept()

                data = conn.recv(1024)

                msg = data.decode()
                
                splitted = re.split(' ',msg)

                verificationDict = {}
                
                for string in splitted:
                    s = re.split(r':',string)
                    if s[0] == 'filename':
                        verificationDict['filename'] = s[1]

                    if s[0] == 'visited':
                        visited = re.split(',',s[1])
                        if '' in visited : visited.remove('')
                        verificationDict['visited'] = visited
                
                #verificar se já tem a stream

                stream = database.getStream(verificationDict['filename'])

                if(stream != False):
                        message = f'time:{time.time()} jumps:{0}'
                        conn.send(message.encode())
                else:
                        result = verifyStreamInNeighbourHood(database, verificationDict['filename'],verificationDict['visited'])
                        if len(result) == 0:
                                message = f'NAK'
                                conn.send(message.encode())
                        else:
                                for response in result:
                                        metricsDict = {}
                                        filename = ""
                                        neighbour = ""
                                        splitted = re.split(' ',response)
                                        s = re.split(r':',splitted)
                                        if s[0] == 'time':
                                                metricsDict['time'] = float(s[1])
                                                metricsDict['timestamp'] = time.time() - float(s[1])
                                        if s[0] == 'jumps':
                                                metricsDict['jumps'] = float(s[1]) + 1
                                        if s[0] == 'neighbour':
                                                neighbour = neighbour + s[1]
                                        if s[0] == 'filename':
                                                filename = filename + s[1]
                                        
                                        database.putRouteStreamDict(filename,neighbour,metricsDict)
                                
                                
                                neighbour = database.getBestMetricsRouteStreamDict(verificationDict['filename'])
                                metrics = database.getMetricsRouteStreamDict(verificationDict['filename'], neighbour)
                                message = f'time:{metrics["time"]} jumps:{metrics["jumps"]}'
                                conn.send(message.encode())

                                        

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
                mynames = getMyNames()

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
                                        

def server(database):
    try:
        SERVER_PORT = 7777
    except:
        print("[Usage: Server.py Server_port]\n")
    rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rtspSocket.bind(('', SERVER_PORT))
    rtspSocket.listen(5)    
    # Receive client info (address,port) through RTSP/TCP session
    while True:
        clientInfo = {}
        clientInfo['rtspSocket'] = rtspSocket.accept()
        ServerWorker.ServerWorker(clientInfo,database).run()           

def clientConnections(database):

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', 2555))  
        server_socket.listen(10)        # 10 conexoes no maximo
        
        while True:
                conn, address = server_socket.accept()  # accept new connection
                port = conn.recv(1024).decode()
                print(port, 'from ' + address[0])
                Thread(target=server, args = (database,)).start()



def receiveVideo(addr, port):
        buffer = []
        socket_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_receive.bind(('', port))
        i = 0
        while True:
                data, address = socket_receive.recvfrom(1024)
                i += 1
                print("i = " + str(i))
                buffer.append(data)
                #print(str(data), flush=True)





if __name__ == '__main__':

        database = database.database()
        bootstrapper = sys.argv[1]
        Thread(target=neighboursRequest, args = (bootstrapper,database)).start()
        Thread(target=clientConnections, args = (database,)).start()
        Thread(target=receiveStreamVerification, args = (database,)).start()
        Thread(target=receiveStreamRequest, args = (database,)).start()        
       

        
        
   






    