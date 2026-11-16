from cairosvg import svg2png
import chess.svg
import pygame

def renderBoard(board):
    boardSVG = chess.svg.board(board, size=600)

    with open("board.svg", "w") as f:
        f.write(boardSVG)

    svg2png(url='board.svg', write_to='board.png')


def displayBoard():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))

    pygame.display.set_caption('Chess Board')

    status = True
    while status:
        try:
            surface = pygame.image.load('board.png').convert()
        except FileNotFoundError:
            pygame.time.delay(50)
            continue

        screen.blit(surface, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False

    pygame.quit()