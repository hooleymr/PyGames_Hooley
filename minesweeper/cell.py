class Piece():
    def __init__(self, hasBomb):
        self.hasBomb = hasBomb
        self.clicked = False
        self.flagged = False
        self.numNearby = 0
        self.nearby = []
    
    def getHasBomb(self):
        return self.hasBomb

    def getClicked(self):
        return self.clicked

    def getFlagged(self):
        return self.flagged

    def getNumNearby(self):
        return self.numNearby

    def setNearby(self, nearby):
        self.nearby = nearby

    def setNumNearby(self): #num bombs around the piece
        num = 0
        for nearby in self.nearby:
            if(nearby.getHasBomb()):
                num += 1
        self.numNearby = num

    def toggleFlagged(self):
        self.flagged = not self.flagged

    def click(self):
        self.clicked = True

    def getListNearby(self):
        return self.nearby

    