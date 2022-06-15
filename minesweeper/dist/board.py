from sqlalchemy import false
from cell import Piece
from random import random


class Board():
    def __init__(self, size, prob):
        self.size = size
        self.prob = prob
        self.lost = False
        self.won = False
        self.numClicked = 0
        self.numNonBombs = 0
        self.setBoard()
        self.setNearby()
        self.setNumNearby()
        

    def setBoard(self):
        self.board = [] #all the same type cell objects

        for row in range(self.size[0]): #size is a tuple
            row = []
            for col in range(self.size[1]): #size is a tuple
                hasBomb = random() < self.prob #if random num is less than prob hasbomb is true
                if (not hasBomb):
                    self.numNonBombs +=1
                cell = Piece(hasBomb)
                row.append(cell)
            self.board.append(row)
        self.setNearby()

    def setNearby(self):
        for row in range(self.size[0]): #size is a tuple
            for col in range(self.size[1]): #size is a tuple
                piece = self.getPiece((row,col))
                nearby = []
                self.getListOfNearby(nearby, row, col)
                piece.setNearby(nearby)       

    def getListOfNearby(self, nearby, row, col): #check surrounding cells for bombs
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r == row and c == col:
                    continue
                if r < 0 or r >= self.size[0] or c < 0 or c >= self.size[1]:
                    continue
                nearby.append(self.board[r][c])

    def setNumNearby(self):
        for row in self.board:
            for piece in row:
                piece.setNumNearby()

    def getSize(self):
        return self.size

    def getPiece(self, index):
        return self.board[index[0]][index[1]]

    def handleClick(self, piece, flag):
        if (piece.getClicked() or (not flag and piece.getFlagged())): #piece is already clicked or already flagged
            return
        if (flag):
            piece.toggleFlagged()
            return
        piece.click()
        if(piece.getHasBomb()):
            self.lost = True #set lost if bomb is clicked
            return
        self.numClicked += 1
        if(piece.getNumNearby() != 0):
            return
        for neighbor in piece.getListNearby():
            if (not neighbor.getHasBomb() and not neighbor.getClicked()):
                self.handleClick(neighbor, False)
        
    def getLost(self): #may be able to consolidate into single win/lose function
        return self.lost
    
    def getWon(self):
        return self.numNonBombs == self.numClicked