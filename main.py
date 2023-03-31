import pygame
from gameplay.CONST import DIM, SIZE
from gameplay.play import Play
from minimax.algorithm import minimax

pygame.init()

# Opens the window in which the game is played
surface = pygame.display.set_mode(DIM)
surface.fill((255,245,238))
pygame.display.set_caption("Checkers")
FPS = 60

# Gets board coordinates given the mouse's coordinates on the screen
def getCoords(pos):
    x, y = pos
    row = y // SIZE
    col = x // SIZE
    return row, col

def main(AI):
    play = True
    clock = pygame.time.Clock()
    play = Play(surface)

    while (play):
        clock.tick(FPS)

        if AI and (play.turn == "red"):
            value, newBoard = minimax(play.getBoard(), 4, True, play)
            play.moveAI(newBoard)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                play = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play.getWinner():
                    play.newGame()
                mouseCoords = pygame.mouse.get_pos()
                row, col = getCoords(mouseCoords)
                play.selectPiece(row, col)

        play.update()

    pygame.quit()

# True to have AI on, False to turn it off
main(False)