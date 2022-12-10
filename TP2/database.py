import socket

class database:
    neighbours : list
    serversNeighbours : list
    serverStatus : dict
    streamsDict : dict
    routeStreamDict : dict

    def __init__(self):
        self.neighbours = []
        self.neighboursConnection = {}
        self.serverStatus = {}
        self.streamsDict = {}

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
    
    #change
    def putStream(self,streamName,metrics):
        self.streamsDict[streamName] = metrics
         

    def putRouteStreamDict(self,filename,neighbour,metrics):
            self.routeStreamDict[filename][neighbour] = metrics

    def getRouteStreamDict(self):
            return self.routeStreamDict
            




