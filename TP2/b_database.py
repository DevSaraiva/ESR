class b_database:
    peersConnected : int
    topo : dict
    file : list

    def __init__(self):
        self.peersConnected = 0
        self.file = []

    def getPeersConnected(self):
        return self.peersConnected
    
    def addPeerConnected(self):
        self.peersConnected = self.peersConnected + 1

    def setTopo(self,topo):
        self.topo =  topo
    
    def getTopo(self):
        return self.topo

    def setFile(self, file):
        self.file = file

    def getFile(self):
        return self.file