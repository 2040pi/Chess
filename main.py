import chess
import drawBoard
import pygame
import engine

board = chess.Board()

pygame.init()
screen = pygame.display.set_mode((600, 600))

pygame.display.set_caption('Chess Board')

status = True
while status:
    board = engine.makeMove(board)
    drawBoard.renderBoard(board)
    surface = pygame.image.load('board.png').convert()
    screen.blit(surface, (0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False

pygame.quit()
