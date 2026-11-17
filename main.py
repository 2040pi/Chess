import chess
import chess.pgn
import engine

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
        board = engine.makeMove(board)
        prevMove = board.pop()
        print(board.san(prevMove))
        board.push(prevMove)