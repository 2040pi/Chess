import chess
import chess.pgn
import engine
import random

board = chess.Board()

computerTurn = random.choice([True, False])

running = True
while running:
    if board.is_game_over():
        if board.is_checkmate():
            print("Checkmate")
        else:
            print("Draw")
        running = False
    else:
        if board.turn == computerTurn:
            board = engine.makeMove(board) 
            prevMove = board.pop()
            print("Computer Move: " + str(prevMove))
            board.push(prevMove)
                    
        else:
            correctMoveEntered = False
            legalMoves = list(board.legal_moves)
            # print(legalMoves)
            while not correctMoveEntered:
                playerMove = input("Input your move: ")
                # playerMove = chess.Move()
                if chess.Move.from_uci(playerMove) in legalMoves:
                    correctMoveEntered = True
                    board.push(chess.Move.from_uci(playerMove))
                else: print("Invalid Move")
                    

pgn = str(chess.pgn.Game.from_board(board))
with open("game.pgn", "w") as f:
    f.write(pgn)
