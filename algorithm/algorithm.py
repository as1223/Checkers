from copy import deepcopy
import pygame

# Applies the minimax algorithm to find the best move available
def minimax(boardState, depth, maximizer, game, difficulty):
    if (depth == 0) or (boardState.getWinner()):
        if (difficulty % 2) == 1:
            return boardState.score(), boardState
        else:
            return boardState.score2(), boardState
    
    # Maximizer tries to maximize score, minimizer tries to minimize it
    if maximizer:
        maxScore = -10000
        bestMove = None
        for move in getMovesPossible(boardState, "red", game):
            newScore = minimax(move, depth-1, False, game, difficulty)[0]
            maxScore = max(maxScore, newScore)
            if (maxScore == newScore):
                bestMove = move
        return maxScore, bestMove
    else:
        minScore = 10000
        bestMove = None
        for move in getMovesPossible(boardState, "black", game):
            newScore = minimax(move, depth-1, True, game, difficulty)[0]
            minScore = min(minScore, newScore)
            if (minScore == newScore):
                bestMove = move
        return minScore, bestMove
    

def simulateMove(piece, move, boardState, game, skip):
    boardState.movePiece(piece, move[0], move[1])
    if skip:
        boardState.removePieces(skip)
    return boardState

def getMovesPossible(boardState, color, game):
    moves = []
    for piece in boardState.colorPieces(color):
        valid = boardState.getValidMoves(piece)
        for move, skip in valid.items():
            # Creates new copy of boardState so that algorithm doesn't alter the actual board while testing moves
            temp = deepcopy(boardState)
            tempPiece = temp.getPiece(piece.row, piece.col)
            newBoardState = simulateMove(tempPiece, move, temp, game, skip)
            moves.append(newBoardState)
    return moves
