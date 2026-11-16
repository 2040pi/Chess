from cairosvg import svg2png
import chess.svg
import pygame

def renderBoard(board):
    boardSVG = chess.svg.board(board, size=600)

    with open("board.svg", "w") as f:
        f.write(boardSVG)

    svg2png(url='board.svg', write_to='board.png')
