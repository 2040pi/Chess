import chess
import chess.pgn
import engine
import time
import eval

board = chess.Board()


longestMoveTime = 0

moveCount = 0
moveTimeTotal = 0

running = True
while running:
    if board.is_game_over():
        if board.is_checkmate():
            print("Checkmate")
        else:
            print("Draw")
        running = False
    else:
        print("Move " + str(board.fullmove_number) + " - " + ("White" if board.turn else "Black"))
        print("Legal Moves = " + str(len(list(board.legal_moves))))
        print("Pieces = " + str(len(board.piece_map())))
        startTime = time.time()
        board = engine.makeMove(board) 
        endTime = time.time()
        moveTimeTotal += endTime-startTime
        moveCount += 1
        if endTime-startTime > longestMoveTime: longestMoveTime = endTime-startTime
        print("Time To Move = ~" + str(int(endTime-startTime)) + "s")
        
        prevMove = board.pop()
        print("Chosen Move = " + board.san(prevMove))
        board.push(prevMove)
        
        print("Board Eval = " + str(eval.eval(board)))
        
        pgn = str(chess.pgn.Game.from_board(board))
        with open("game.pgn", "w") as f:
            f.write(pgn)        
        
        print("\n")

print(board)

print("Longest Move Time = " + str(longestMoveTime) + "s")
print("Average Move Time = " + str(moveTimeTotal/moveCount) + "s")

pgn = str(chess.pgn.Game.from_board(board))
with open("game.pgn", "w") as f:
    f.write(pgn)
