import chess
import tables

def orderedMoves(board: chess.Board):
   legalMoves = list(board.legal_moves)
   orderedMoves = sorted(legalMoves, key=lambda x: -quickEval(board, x))
   return orderedMoves


def quickEval(board: chess.Board, move):
  score = 0

  if board.is_capture(move):
    if board.is_en_passant(move):
      score += tables.pieceValues[chess.PAWN]
    else:
      score += tables.pieceValues[board.piece_at(move.to_square).piece_type]

  if board.gives_check(move):
    score += 50

  if move.promotion is not None:
    score += tables.pieceValues[move.promotion]

  return score