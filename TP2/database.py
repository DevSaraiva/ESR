import socket
import traceback
from time import sleep


class database:
    neighbours : list #lista de neighbours
    serversNeighbours : list #list of servers in neighbourhood
    serverStatus : dict #metrics of server connection in neighbourhood
    streamsDict : dict #dict of streams in the node
    routeStreamDict : dict #metrics of streams in neighbourhood


    def __init__(self):
        self.neighbours = []
        self.serverStatus = {}
        self.streamsDict = {}
        self.routeStreamDict = {}
        self.metricsInNeighbourhood = {}

    def putServersNeighbours(self,neighbours):
        self.serversNeighbours = neighbours

    def getServersNeighbours(self):
        return self.neighbours

    def putNeighbours(self,neighbours):
        self.neighbours = neighbours

    def getNeighbours(self):
        return self.neighbours

    def putConnectionServerStatus(self,neighbour,connection):

        if neighbour in  self.serverStatus.keys():
            if self.serverStatus[neighbour]['servername'] != connection['servername']:
                if abs(self.serverStatus[neighbour]['timestamp'] - connection['timestamp']) < 0.1 * min(self.serverStatus[neighbour]['timestamp'],connection['timestamp']):
                        if (self.serverStatus[neighbour]['jumps'] > connection['jumps']):
                            self.serverStatus[neighbour] = connection          
                elif self.serverStatus[neighbour]['timestamp'] > connection['timestamp']:
                    self.serverStatus[neighbour] = connection 
        else:
            self.serverStatus[neighbour] = connection

    def getConnectionServerStatus(self,neighbour):
        return self.serverStatus[neighbour]

    def getStream(self,streamName):
        if(streamName in self.streamsDict.keys()):
            if self.streamsDict[streamName]['state'] == 'activated': return self.streamsDict[streamName]
            else: return False
        else:
            return False
    def getStreamState(self,streamName):
            if(streamName in self.streamsDict.keys()):
                return self.streamsDict[streamName]['state']
            else: return False

    def changeStreamState(self,streamName,state):
            if(streamName in self.streamsDict.keys()):
                self.streamsDict[streamName]['state'] = state
            else: return False
    
    def putStreamEmpty(self,streamName):
        dic = {}
        dic['state'] = 'activated'
        dic['receivers'] = []
        dic['clients'] = {}
        self.streamsDict[streamName] = dic

    def addStreamReceiver(self,streamName,ip):
        try:
            if self.streamsDict[streamName]['state'] == 'activated':
                self.streamsDict[streamName]['receivers'].append(ip)
            else : return False
        except Exception: 
            return False

    def removeStreamReceiver(self,streamName,ip):
        try:
            self.streamsDict[streamName]['receivers'].remove(ip)

            if len(self.streamsDict[streamName]['receivers']) == 0 and len(self.streamsDict[streamName]['clients'].keys()) == 0:
                self.streamsDict[streamName]['state'] = 'disabled'
                print(self.streamsDict[streamName]['state'])

        except Exception: 
            return False
    
    def getStreamReceivers(self,streamName):
        try:
            return self.streamsDict[streamName]['receivers']
            
        except Exception: 
            return False

    
    def addStreamClient(self,streamName,ip):
        try:
            if self.streamsDict[streamName]['state'] == 'activated':
                self.streamsDict[streamName]['clients'][ip] = []
            else: return False
        except :
            return False

    def removeStreamClient(self,streamName,ip):
        try:
            self.streamsDict[streamName]['clients'].pop(ip, None)
            if len(self.streamsDict[streamName]['receivers']) == 0 and len(self.streamsDict[streamName]['clients'].keys()) == 0:
                self.streamsDict[streamName]['state'] = 'disabled'
                print(self.streamsDict[streamName]['state'])
            print('poped')
        except :
            return False

    def getStreamClients(self,streamName):
        return self.streamsDict[streamName]['clients'].keys()

    
    def putStreamPacket(self,streamName,ip,packet):
        
        try:
            self.streamsDict[streamName]['clients'][ip].append(packet)
        except:
            pass
        

    def popStreamPacket(self,streamName,ip):
        try:
                return self.streamsDict[streamName]['clients'][ip].pop(0)
        except Exception:
            # traceback.print_exc()
            return None
         

    def getBestMetricsServerStatus(self,comeFrom):
        
            timestamp = 9999999999
            neighbourAux = ''
            jumps = 9999999999
            for neighbour in self.serverStatus.keys():
                if(neighbour not in comeFrom):
                    if abs(self.serverStatus[neighbour]['timestamp'] - timestamp) < 0.1 * min(self.serverStatus[neighbour]['timestamp'],timestamp):
                        if (self.serverStatus[neighbour]['jumps'] < jumps):
                            neighbourAux = neighbour
                            timestamp = self.serverStatus[neighbour]['timestamp']
                            jumps = self.serverStatus[neighbour]['jumps']    
                    elif self.serverStatus[neighbour]['timestamp'] < timestamp:
                        neighbourAux = neighbour
                        timestamp = self.serverStatus[neighbour]['timestamp'] 
                        jumps = self.serverStatus[neighbour]['jumps']
                
                
        
                
            return neighbourAux
    
   

    def putRouteStreamDict(self,filename,neighbour,metrics):
            if filename in self.routeStreamDict.keys():
                self.routeStreamDict[filename][neighbour] = metrics
            else :
                self.routeStreamDict[filename] = {}
                self.routeStreamDict[filename][neighbour] = metrics

    
    def getBestMetricsRouteStreamDict(self,filename):
            dict =  self.routeStreamDict[filename]

            print('getttttttttttttttttttttttttttt',flush=True)

            timestamp = 9999999999
            neighbourAux = ''
            jumps = 9999999999
            for neighbour in dict.keys():
                print(dict[neighbour]['timestamp'],timestamp)
                if abs(dict[neighbour]['timestamp'] - timestamp) < 0.1 * min(dict[neighbour]['timestamp'],timestamp):
                    if dict[neighbour]['jumps'] < jumps:
                        timestamp = dict[neighbour]['timestamp']
                        neighbourAux = neighbour
                        jumps = dict[neighbour]['jumps']
                elif dict[neighbour]['timestamp'] < timestamp:
                    neighbourAux = neighbour
                    timestamp = dict[neighbour]['timestamp']
                    jumps = dict[neighbour]['jumps']

                print(neighbour, neighbourAux,flush=True)
            
            return neighbourAux
    
    def getNumberOfRouteStream(self,filename):
        if filename in self.routeStreamDict.keys():
            return len(self.routeStreamDict[filename].keys())
        else: return 0
                
            

    def getMetricsRouteStreamDict(self,filename, neighbour):
            return self.routeStreamDict[filename][neighbour]

            




