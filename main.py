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

def main():
    play = True
    clock = pygame.time.Clock()
    play = Play(surface)

    while (play):
        clock.tick(FPS)
        
        pygame.image.save(surface, "screenshot.jpeg")

        if (play.turn == "red"):
            value, newBoard = minimax(play.getBoard(), ((play.getDifficulty()+1)//2), True, play, play.getDifficulty())
            play.moveAI(newBoard)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play.getWinner():
                    play.newGame(play.getWinner())
                mouseCoords = pygame.mouse.get_pos()
                row, col = getCoords(mouseCoords)
                if (row < 8) and (col < 8):
                    play.selectPiece(row, col)

        play.update()
        print(play.getDifficulty())

    pygame.quit()

main()
