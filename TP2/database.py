import socket

class database:
    neighbours : list
    serversNeighbours : list
    serverStatus : dict

    def __init__(self):
        self.neighbours = []
        self.neighboursConnection = {}
        self.serverStatus = {}

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
            


