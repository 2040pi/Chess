import chess
import minimax

# TODO - Add Endgame Tables

def makeMove(board: chess.Board):
    legal_moves = list(board.legal_moves)

    if len(legal_moves) == 1:
        board.push(legal_moves[0])
        return board
    piece_count = len(board.piece_map())
    if piece_count <= 8 and len(legal_moves) <= 8:
        depth = 10
    elif piece_count <= 12 and len(legal_moves) <= 12:
        depth = 5
    elif piece_count <= 16 and len(legal_moves) <= 16:
        depth = 4
    else:
        depth = 3

    isWhiteTurn = board.turn == chess.WHITE
    bestMove = minimax.minimax_root(depth, board, is_maximising_player=isWhiteTurn)

    board.push(bestMove)
    return board

