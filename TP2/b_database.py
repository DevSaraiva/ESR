class b_database:
    peersConnected : int
    topo : dict

    def __init__(self):
        self.peersConnected = 0

    def getPeersConnected(self):
        return self.peersConnected
    
    def addPeerConnected(self):
        self.peersConnected = self.peersConnected + 1

    def setTopo(self,topo):
        self.topo =  topo
    
    def getTopo(self):
        return self.topo



