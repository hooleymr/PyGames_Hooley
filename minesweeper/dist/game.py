from tokenize import String
from turtle import position, right
import pygame
from cell import Piece
import board
import os

class Game():
    def __init__(self, board, screenSize):
        self.board = board
        self.screenSize = screenSize
        self.pieceSize = self.screenSize[0] // self.board.getSize()[1], self.screenSize[1] // self.board.getSize()[0] #width/num cols and height/num rows
        self.loadImages()

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screenSize)
        running = True
        while running: #cant do while true for some reason, pygame.quit becomes unreachable
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    running = False
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    position = pygame.mouse.get_pos()
                    rightClick = pygame.mouse.get_pressed()[2] #check if mouse click was right click
                    self.handleClick(position, rightClick)
            self.draw() #draw squares
            pygame.display.flip()
            if(self.board.getWon()):
                running = False
        pygame.quit()
            
    def draw(self): #self.board.getSize()[0] = rows -------- self.board.getSize()[1] = cols
        topLeft = (0,0)
        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                piece = self.board.getPiece((row,col))
                image = self.getImage(piece)
                self.screen.blit(image, topLeft)
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1] #shift right
            topLeft = 0, topLeft[1] + self.pieceSize[1] #shift down and back to the left

    def loadImages(self):
        self.images = {} #dict to tie tile png to game value
        for fileName in os.listdir("images"):
            if (not fileName.endswith(".png")): #file name does not end with png skip this file
                continue
            image = pygame.image.load(r"images/" + fileName)
            image = pygame.transform.scale(image, self.pieceSize)
            self.images[fileName.split(".")[0]] = image

    def getImage(self, piece):
        string = None
        if (piece.getClicked()):
            if piece.getHasBomb():
                string = "bomb"
            else:
                string = str(piece.getNumNearby())
        else:
            string = "flag" if piece.getFlagged() else "init"

        return self.images[string]

    def handleClick(self, position, rightClick):
        if(self.board.getLost()): #if game is lost can no longer click
            return
        index = position[1] // self.pieceSize[1], position[0] // self.pieceSize[0] #posy / cell width , posx / cell height 
        #print(index)
        piece = self.board.getPiece(index)
        self.board.handleClick(piece, rightClick)