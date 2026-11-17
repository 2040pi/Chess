import chess
import minimax

def makeMove(board: chess.Board):
    legal_moves = list(board.legal_moves)

    if len(legal_moves) == 1:
        board.push(legal_moves[0])
        return board

    piece_count = len(board.piece_map())
    if piece_count <= 6:
        depth = 6
    elif piece_count <= 9:
        depth = 5
    elif piece_count <= 12:
        depth = 4
    else:
        depth = 3

    isWhiteTurn = board.turn == chess.WHITE
    bestMove = minimax.minimax_root(depth, board, is_maximising_player=isWhiteTurn)

    board.push(bestMove)
    return board

