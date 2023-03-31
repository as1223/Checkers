import pygame
from .CONST import SIZE, RED, RED_KING, BLACK, BLACK_KING

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.selected = False

        # Screen coordinates    
        self.x = 0
        self.y = 0
        self.getPos()

    # Gets screen coordinates of top-left corner of current square
    def getPos(self):
        self.x = SIZE * self.col
        self.y = SIZE * self.row

    # Called when a piece reaches the other end of the board
    def reachedKing(self):
        self.king = True

    # Draws piece using image files
    def draw(self, screen):
        if (self.color == "red"):
            if (self.king):
                screen.blit(RED_KING, (self.x, self.y))
            else:
                screen.blit(RED, (self.x, self.y))
        else:
            if (self.king):
                screen.blit(BLACK_KING, (self.x, self.y))
            else:
                screen.blit(BLACK, (self.x, self.y))

        # Hightlights selected piece
        if self.selected:
            pygame.draw.rect(screen, (65,105,225), (self.x, self.y, SIZE, SIZE), 3) 

    # Moves piece to specified location
    def move(self, row, col):
        self.row = row
        self.col = col
        self.getPos()