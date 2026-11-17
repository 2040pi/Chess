import chess
import tables

def makeMove(board: chess.Board):
    isWhiteTurn = board.turn == chess.WHITE
    depth = 0
    if len(list(board.legal_moves)) > 10:
      depth = 3
    else:
      depth = 4
    bestMove = minimax_root(depth, board, is_maximising_player =isWhiteTurn)

    board.push(bestMove)
    return board


def eval(board):
    if board.is_checkmate():
        return -99999 if board.turn == chess.WHITE else 99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = tables.pieceValues[piece.piece_type]
            if piece.color == chess.WHITE:
                sqaureValue = tables.blendTables(piece.piece_type, True, board.fullmove_number)[square]
                score += value
                score += sqaureValue
            else:
                sqaureValue = tables.blendTables(piece.piece_type, False, board.fullmove_number)[square]
                score -= value
                score -= sqaureValue
                
    return score

def orderedMoves(board: chess.Board):
   legalMoves = list(board.legal_moves)
   orderedMoves = sorted(legalMoves, key=lambda x: quickEval(board, x))
   return orderedMoves

def quickEval(board: chess.Board, move):
  if board.is_capture(move):
    if board.is_en_passant(move):
      return chess.PAWN
    else:
      return tables.pieceValues[board.piece_at(move.to_square).piece_type]
  return 0

def minimax(depth, board, alpha, beta, is_maximising_player):
  if depth == 0 or board.is_game_over():
    return eval(board)

  legal_moves = orderedMoves(board)
  if not legal_moves:
    return eval(board)

  if(is_maximising_player):
    best_move = -99999
    for move in legal_moves:
      board.push(move)
      best_move = max(best_move, minimax(depth-1, board, alpha, beta, not is_maximising_player))
      board.pop()
      alpha = max(alpha, best_move)
      if(beta <= alpha):
        return best_move
    return best_move
  else:
    best_move = 99999
    for move in legal_moves:
      board.push(move)
      best_move = min(best_move, minimax(depth-1, board, alpha, beta, not is_maximising_player))
      board.pop()
      beta = min(beta, best_move)
      if(beta <= alpha):
        return best_move
    return best_move


def minimax_root(depth, board, is_maximising_player = True):
  legal_moves = orderedMoves(board)
  best_move = -99999 if is_maximising_player else 99999
  best_move_found = None

  for move in legal_moves:
    board.push(move)
    value = minimax(depth - 1, board, -99999, 99999, not is_maximising_player)
    board.pop()
    if (is_maximising_player and value >= best_move) or (not is_maximising_player and value <= best_move):
      best_move = value
      best_move_found = move

  return best_move_found
