class b_database:
    peersConnected : int

    def __init__(self):
        self.peersConnected = 0

    def getPeersConnected(self):
        return self.peersConnected
    
    def addPeerConnected(self):
        self.peersConnected = self.peersConnected + 1


