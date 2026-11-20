import chess

def attacked_squares(board: chess.Board, color: chess.Color):
    attacked = chess.SquareSet()
    for attacker in chess.SquareSet(board.occupied_co[color]):
        attacked |= board.attacks(attacker)
    return attacked

board = chess.Board()
print(attacked_squares(board=board, color=board.turn))
print(len(attacked_squares(board=board, color=board.turn)))