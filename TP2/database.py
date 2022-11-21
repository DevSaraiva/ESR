class database:
    neighbours : list

    def __init__(self):
        self.neighbours = []

    def putNeighbours(self,neighbours):
        self.neighbours = neighbours

    def getNeighbours(self):
        return self.neighbours

