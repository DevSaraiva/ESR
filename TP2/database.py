import socket
import traceback


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
        self.serverStatus[neighbour] = connection

    def getConnectionServerStatus(self,neighbour):
        return self.serverStatus[neighbour]

    def getStream(self,streamName):
        if(streamName in self.streamsDict.keys()):
            return self.streamsDict[streamName]
        else:
            return False
    def getStreamState(self,streamName):
            if(streamName in self.streamsDict.keys()):
                return self.streamsDict[streamName]['state']
            else: return False
    
    def putStreamEmpty(self,streamName):
        dic = {}
        dic['queue'] = []
        dic['state'] = 'activated'
        dic['receivers'] = 0
        dic['receiversDict'] = {}
        self.streamsDict[streamName] = dic

    def addStreamReceiver(self,streamName):
        try:
            self.streamsDict[streamName]['receiversDict'][f'{self.streamsDict[streamName]["receivers"]}'] = 0
            self.streamsDict[streamName]['receivers'] = self.streamsDict[streamName]['receivers'] + 1
            print('addReceiver ' + streamName)
            return f'{self.streamsDict[streamName]["receivers"] - 1}'
        
        except Exception: 
            return False

    def putStreamPacket(self,streamName,packet):
        self.streamsDict[streamName]['queue'].append(packet)
        

    def popStreamPacket(self,streamName,receiverID):
        try:
            print(receiverID)
            if receiverID == -1 : 
                return None
            
            if self.streamsDict[streamName]['receivers'] == 1:
                # print(receiverID  + ' Pop')
                return self.streamsDict[streamName]['queue'].pop(0)
            else :
                # print(receiverID  + ' notPop')
                self.streamsDict[streamName]['receiversDict'][receiverID] = self.streamsDict[streamName]['receiversDict'][receiverID] +1 
                return self.streamsDict[streamName]['queue'][self.streamsDict[streamName]['receiversDict'][receiverID] - 1]
        except Exception: 
            # print('EXCEPTION ',receiverID)
            return None
         

    def getBestMetricsServerStatus(self):
        
            timestamp = 9999999999
            neighbourAux = ''
            for neighbour in self.serverStatus.keys():
                if self.serverStatus[neighbour]['timestamp'] < timestamp:
                    neighbourAux = neighbour
                    timestamp = self.serverStatus[neighbour]['timestamp'] 
                #aproximadamente igual
            
            return neighbourAux
    
   

    def putRouteStreamDict(self,filename,neighbour,metrics):
            if filename in self.routeStreamDict.keys():
                self.routeStreamDict[filename][neighbour] = metrics
            else :
                self.routeStreamDict[filename] = {}
                self.routeStreamDict[filename][neighbour] = metrics

    
    def getBestMetricsRouteStreamDict(self,filename):
            dict =  self.routeStreamDict[filename]

            timestamp = 9999999999
            neighbourAux = ''
            for neighbour in dict.keys():
                if dict[neighbour]['timestamp'] < timestamp:
                    neighbourAux = neighbour
                    timestamp = dict[neighbour]['timestamp'] 
                #aproximadamente igual
            
            return neighbourAux
    
    def getNumberOfRouteStream(self,filename):
        if filename in self.routeStreamDict.keys():
            return len(self.routeStreamDict[filename].keys())
        else: return 0
                
            

    def getMetricsRouteStreamDict(self,filename, neighbour):
            return self.routeStreamDict[filename][neighbour]

            




