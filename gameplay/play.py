import pygame
from .CONST import SIZE
from .board import Board

class Play:
    def __init__(self, screen):
        self.selected = None
        self.board = Board()
        self.turn = "black"
        self.validMoves = {}
        self.screen = screen

        self.win = 0
        self.loss = 0
        f = open("stats.txt", "r")
        record = f.read()
        self.win = record.count('W')
        self.loss = record.count('L')
        self.difficulty = 1
        self.difficulty = self.difficulty + record.count('I') - record.count('D')

    # Updates any changes made to the board
    def update(self):
        self.board.draw(self.screen)
        self.showValid(self.validMoves)
        font = pygame.font.SysFont('Comic Sans MS', 100)
        text = font.render((str(self.win) + " - " + str(self.loss)), False, (0, 0, 0))
        self.screen.blit(text, (850, 200))

        if (self.getWinner() != None):
            font = pygame.font.SysFont('Comic Sans MS', 100)
            text = font.render(self.getWinner() + " wins!", False, (0, 0, 0))
            self.screen.blit(text, (150, 300))

        pygame.display.update()

    # Returns board
    def getBoard(self):
        return self.board

    # Selects a piece on the board based on user input
    def selectPiece(self, row, col):
        # If a piece is already selected, move it to the selected destination
        if self.selected:
            moved = self._move(row, col)
            # If unable to move to the selected destination, assume the user is trying to select a different piece instead of moving the selected one
            if not moved:
                self.selected.selected = False
                self.selected = None
                self.validMoves = {}
                self.selectPiece(row, col)

        piece = self.board.getPiece(row, col)
        # If a piece that is allowed to move (same color as turn) is selected, update its valid moves
        if (piece != 0) and (piece.color == self.turn):
            self.selected = piece
            self.selected.selected = True #####
            self.validMoves = self.board.getValidMoves(piece)
            #print(len(self.validMoves))
            return True
        
        return False

    # Moves piece if possible, removes any captured pieces, and switches turn
    def _move(self, row, col):
        piece = self.board.getPiece(row, col)
        # Checks if a piece already selected and the destination is empty and valid
        if (self.selected) and (piece == 0) and ((row, col) in self.validMoves):
            # Moves piece
            self.board.movePiece(self.selected, row, col)
            # Removes captured pieces
            captured = self.validMoves[(row, col)]
            if captured:
                self.board.removePieces(captured)
            # Ends turn and lets other player move
            self.changeTurn()
        else:
            # Move wasn't made
            return False
        
        return True
    
    # Shows the player what moves are available for the selected piece
    def showValid(self, moves):
        for m in moves:
            row, col = m
            pygame.draw.circle(self.screen, (65,105,225), (col*SIZE + SIZE//2, row*SIZE + SIZE//2), 15)
    
    def changeTurn(self):
        if (self.turn == "red"):
            self.turn = "black"
        else:
            self.turn = "red"
        self.validMoves = {}

    # Returs winner if one exists
    def getWinner(self):
        if (self.board.getRed() == 0):
            self.board.setWinner("black")
            return "black"
        if (self.board.getBlack() == 0):
            self.board.setWinner("red")
            return "red"
        # Check for current turn's pieces all having no valid moves. Other player wins in this case.
        if (self.turn == "red"):
            able = False
            pieces = self.board.colorPieces("red")
            for p in pieces:
                if (len(self.board.getValidMoves(p)) != 0):
                    able = True
                    break
            if not able:
                self.board.setWinner("black")
                return "black"
        if (self.turn == "black"):
            able = False
            pieces = self.board.colorPieces("black")
            for p in pieces:
                if (len(self.board.getValidMoves(p)) != 0):
                    able = True
                    break
            if not able:
                self.board.setWinner("red")
                return "red"
        return None

    # Resets the game with initial values
    def newGame(self, winner):
        self.selected = None
        self.board = Board()
        self.turn = "black"
        self.validMoves = {}
        f = open("stats.txt", "a")
        if winner == "black":
            self.win = self.win + 1
            f.write("W")
        else: 
            self.loss = self.loss + 1
            f.write("L")
        f.close()
        self.updateDifficulty()

    def updateDifficulty(self):
        f = open("stats.txt", "r")
        record = f.read()
        if (len(record) >= 4):
            last4 = record[-4:]
            if (last4 == "WWWW" and self.difficulty < 8):
                self.difficulty = self.difficulty + 1
                f = open("stats.txt", "a")
                f.write("I")
                f.close()
                return
            if (last4 == "LLLL" and self.difficulty > 1):
                self.difficulty = self.difficulty - 1
                f = open("stats.txt", "a")
                f.write("D")
                f.close()
                return
        if len(record) < 5:
            return
        last5 = record[-5:]
        if (last5.count('I') > 0) or (last5.count('D') > 0):
            return
        f.close()
        wins = last5.count('W')
        if (wins >= 4 and self.difficulty < 8):
            self.difficulty = self.difficulty + 1
            f = open("stats.txt", "a")
            f.write("I")
            f.close()
        if (wins <= 1 and self.difficulty > 1):
            self.difficulty = self.difficulty - 1
            f = open("stats.txt", "a")
            f.write("D")
            f.close()

    def getDifficulty(self):
        return self.difficulty

    # Updates the board with the AI move made
    def moveAI(self, board):
        self.board = board
        self.changeTurn()
