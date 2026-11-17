import chess
import chess.pgn
import drawBoard
import pygame
import engine
import time

board = chess.Board()

pygame.init()
screen = pygame.display.set_mode((600, 600))

pygame.display.set_caption('Chess Board')

status = True
while status:
    drawBoard.renderBoard(board)
    surface = pygame.image.load('board.png').convert()
    screen.blit(surface, (0, 0))
    pygame.display.flip()


    isOver = False
    resultString = ""
    if board.can_claim_draw():
        resultString = "Draw"
    elif board.is_game_over():
        resultString = "Checkmate - "
        resultString += "White Wins" if board.outcome().winner else "Black Wins"
        isOver = True
    if isOver:
        print(board)
        print(resultString)
        pgn = str(chess.pgn.Game.from_board(board))
        with open("game.pgn", "w") as f:
            f.write(pgn)
        break
    else:
        startTime = time.time()
        board = engine.makeMove(board)
        endTime = time.time()
        print(endTime-startTime)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False

input("Press enter to quit.")
pygame.quit()
