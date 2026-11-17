import chess
import chess.pgn
import engine
import time

board = chess.Board()

status = True
while status:
    if board.is_game_over():
        print(board)
        pgn = str(chess.pgn.Game.from_board(board))
        with open("game.pgn", "w") as f:
            f.write(pgn)
        break
    else:
        print("Move " + str(board.fullmove_number) + " - " + ("White" if board.turn else "Black"))
        startTime = time.time()
        board = engine.makeMove(board)
        endTime= time.time()
        print("Time To Move = ~" + str(int(endTime-startTime)) + "s")

        prevMove = board.pop()
        print("#Legal Moves = " + str(len(list(board.legal_moves))))
        print("Chosen Move = " + board.san(prevMove))
        board.push(prevMove)