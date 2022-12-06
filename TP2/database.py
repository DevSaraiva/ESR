class database:
    neighbours : list
    neighboursConnection : dict

    def __init__(self):
        self.neighbours = []
        self.neighboursConnection = {}


    def putNeighbours(self,neighbours):
        self.neighbours = neighbours

    def getNeighbours(self):
        return self.neighbours

    def putConnection(self,neighbour,connection):
        self.neighboursConnection[neighbour] = connection

    def getConnection(self,neighbour):
        if neighbour in self.neighboursConnection.keys():
            return self.neighboursConnection[neighbour]
        else:
            return True


