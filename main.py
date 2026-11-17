import chess
import chess.pgn
import engine
import time

board = chess.Board()

status = True
longestMoveTime = 0
while status:
    if board.is_game_over():
        break
    else:
        print("Move " + str(board.fullmove_number) + " - " + ("White" if board.turn else "Black"))
        startTime = time.time()
        board = engine.makeMove(board)
        endTime= time.time()
        if endTime-startTime > longestMoveTime: longestMoveTime = endTime-startTime
        print("Time To Move = ~" + str(int(endTime-startTime)) + "s")

        prevMove = board.pop()
        print("#Legal Moves = " + str(len(list(board.legal_moves))))
        print("Chosen Move = " + board.san(prevMove))
        board.push(prevMove)

print(board)

print("Longest Move Time = " + str(longestMoveTime) + "s")

pgn = str(chess.pgn.Game.from_board(board))
with open("game.pgn", "w") as f:
    f.write(pgn)
