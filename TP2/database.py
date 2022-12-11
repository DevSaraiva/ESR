import socket

class database:
    neighbours : list
    serversNeighbours : list
    serverStatus : dict
    streamsDict : dict
    routeStreamDict : dict
    i : int

    def __init__(self):
        self.neighbours = []
        self.neighboursConnection = {}
        self.serverStatus = {}
        self.streamsDict = {}
        self.i = 0

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
        self.streamsDict[streamName] = dic

    def putStreamPacket(self,streamName,packet):
        self.streamsDict[streamName]['queue'].append(packet)
        

    def popStreamPacket(self,streamName):
        try:
            return self.streamsDict[streamName]['queue'].pop(0)
        except: return None
         

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
            if filename in self.routeStreamDict.keys:
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
                
            

    def getMetricsRouteStreamDict(self,filename, neighbour):
            return self.routeStreamDict[filename][neighbour]
            




