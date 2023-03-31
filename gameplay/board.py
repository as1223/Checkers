import pygame
from .CONST import BOARD_BLACK, BOARD_RED, SIZE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []

        # Number of pieces
        self.redRemaining = 12
        self.blackRemaining = 12
        self.redKings = 0
        self.blackKings = 0

        self.winner = None

        # Adds initial pieces to board
        self.loadBoard()

    # Loads the board at the start of each game
    def drawBoard(self, screen):
        screen.fill(BOARD_BLACK)
        for i in range(8):
            for j in range(8):
                if (i+j) % 2 == 0:
                    pygame.draw.rect(screen, BOARD_RED, (SIZE*j, SIZE*i, SIZE, SIZE))

    # Creates the 2D array for the board, with a Piece in its starting locations or 0 if empty
    def loadBoard(self):
        for i in range(8):
            self.board.append([])
            for j in range(8):
                # Checks for every square that a piece is able to be on (black squares)
                if (j % 2) != (i % 2):
                    # Top half of board (Rows 0, 1, 2)
                    if i <= 2:
                        self.board[i].append(Piece(i, j, "red"))
                    # Bottom half of board (Rows 5, 6, 7)
                    elif i > 4:
                        self.board[i].append(Piece(i, j, "black"))
                    else:
                        self.board[i].append(0)
                else:
                    self.board[i].append(0)

    # Draws board as well as all pieces
    def draw(self, screen):
        self.drawBoard(screen)
        for i in range(8):
            for j in range(8):
                if (self.board[i][j] != 0):
                    self.board[i][j].draw(screen)

    # Moves pieces on the board
    def movePiece(self, piece, row, col):
        # Swaps current location with new location and updates piece's attributes
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        piece.selected = False

        # Checks for king
        if ((row == 0) or (row == 7)) and (not (piece.king)):
            piece.reachedKing()
            if (piece.color == "red"):
                self.redKings += 1
            else:
                self.blackKings += 1

    # Returns the piece at the given row and column
    def getPiece(self, row, col):
        return self.board[row][col]
    
    #
    def getValidMoves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        # Black pieces and kings can move upwards. Check for any valid moves in the two rows above
        if (piece.color == "black") or (piece.king):
            moves.update(self._goLeft(row-1, max(row-3, -1), -1, piece.color, left, piece.king))
            moves.update(self._goRight(row-1, max(row-3, -1), -1, piece.color, right, piece.king))
        # Red pieces and kings can move downwards. Check for any valid moves in the two rows below
        if (piece.color == "red") or (piece.king):
            moves.update(self._goLeft(row+1, min(row+3, 8), 1, piece.color, left, piece.king))
            moves.update(self._goRight(row+1, min(row+3, 8), 1, piece.color, right, piece.king))

        return moves

    # Checks for valid moves to the left of the selected piece
    def _goLeft(self, start, stop, direction, color, left, king, captured=[]):
        moves = {}
        last = []
        for r in range(start, stop, direction):
            # End if reached left of board while checking to the left
            if (left < 0):
                break

            current = self.getPiece(r, left)
            # If currently checked square is empty...
            if (current == 0):
                # If a piece has already been taken, the next jump has to capture another piece, can't go just one square
                if captured and not last:
                    break
                # Second jump possible, check for another jump next
                elif captured:
                    moves[(r, left)] = last + captured
                # No piece captured from this move but still able to move once this way
                else:
                    moves[(r, left)] = last

                if last:
                    row = 0
                    if (direction == -1):
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, 8)
                    # Check for multiple jumps in a turn
                    moves.update(self._goLeft(r+direction, row, direction, color, left-1, king, captured=last))
                    moves.update(self._goRight(r+direction, row, direction, color, left+1, king, captured=last))
                    # Kings can go both directions in a single turn
                    if king:
                        row = 0
                        if (direction == 1):
                            row = max(r-3, -1)
                        else:
                            row = min(r+3, 8)
                        # Only check one direction so that it doesn't keep capturing the same piece over and over
                        moves.update(self._goLeft(r-direction, row, -direction, color, left-1, king, captured=last))
                break
            # If currently checked square is same color as piece being moved, can't move there
            elif (current.color == color):
                break
            # If not empty and not piece with same color, has to be opponent's piece
            else:
                last = [current]

            # Continue checking squares to the left
            left -= 1

        return moves

    # Checks for valid moves to the right of the selected piece
    def _goRight(self, start, stop, direction, color, right, king, captured=[]):
        moves = {}
        last = []
        for r in range(start, stop, direction):
            # End if reached right of board while checking to the right
            if (right > 7):
                break

            current = self.getPiece(r, right)
            # If currently checked square is empty...
            if (current == 0):
                # If a piece has already been taken, the next jump has to capture another piece, can't go just one square
                if captured and not last:
                    break
                # Second jump possible, check for another jump next
                elif captured:
                    moves[(r, right)] = last + captured
                # No piece captured from this move but still able to move once this way
                else:
                    moves[(r, right)] = last

                if last:
                    row = 0
                    if (direction == -1):
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, 8)
                    # Check for multiple jumps in a turn
                    moves.update(self._goLeft(r+direction, row, direction, color, right-1, king, captured=last))
                    moves.update(self._goRight(r+direction, row, direction, color, right+1, king, captured=last))
                    # Kings can go both directions in a single turn
                    if king:
                        row = 0
                        if (direction == 1):
                            row = max(r-3, -1)
                        else:
                            row = min(r+3, 8)
                        # Only check one direction so that it doesn't keep capturing the same piece over and over
                        moves.update(self._goRight(r-direction, row, -direction, color, right+1, king, captured=last))
                break
            # If currently checked square is same color as piece being moved, can't move there
            elif (current.color == color):
                break
            # If not empty and not piece with same color, has to be opponent's piece
            else:
                last = [current]

            # Continue checking squares to the right
            right += 1

        return moves
    
    # Removes pieces from the 2D array if captured (sets them to 0)
    def removePieces(self, pieces):
        for p in pieces:
            self.board[p.row][p.col] = 0
            if (p != 0):
                if (p.color == "red"):
                    self.redRemaining -= 1
                else:
                    self.blackRemaining -= 1

    # Used by getWinner() in play.py
    def getRed(self):
        return self.redRemaining
    def getBlack(self):
        return self.blackRemaining
    def setWinner(self, win):
        self.winner = win
    def getWinner(self):
        return self.winner
    
    # Gets a "score" for the AI to use when determining if a move is good or bad
    def score(self):
        return self.redRemaining - self.blackRemaining
    
    # Returns all pieces of a certain color for the AI to check the "score" of different moves
    def colorPieces(self, color):
        pieces = []
        for i in range(8):
            for j in range(8):
                piece = self.getPiece(i, j)
                if (piece != 0) and (piece.color == color):
                    pieces.append(piece)
        return pieces