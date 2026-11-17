import eval
import preorderMoves

def minimax(depth, board, alpha, beta, is_maximising_player):
  if depth == 0 or board.is_game_over():
    return eval.eval(board)

  legal_moves = preorderMoves.orderedMoves(board)
  if not legal_moves:
    return eval(board)

  if(is_maximising_player):
    best_move = -999999
    for move in legal_moves:
      board.push(move)
      best_move = max(best_move, minimax(depth-1, board, alpha, beta, not is_maximising_player))
      board.pop()
      alpha = max(alpha, best_move)
      if(beta <= alpha):
        return best_move
    return best_move
  else:
    best_move = 999999
    for move in legal_moves:
      board.push(move)
      best_move = min(best_move, minimax(depth-1, board, alpha, beta, not is_maximising_player))
      board.pop()
      beta = min(beta, best_move)
      if(beta <= alpha):
        return best_move
    return best_move


def minimax_root(depth, board, is_maximising_player = True):
  legal_moves = preorderMoves.orderedMoves(board)
  best_move = -999999 if is_maximising_player else 999999
  best_move_found = None

  for move in legal_moves:
    board.push(move)
    value = minimax(depth - 1, board, -99999, 99999, not is_maximising_player)
    board.pop()
    if (is_maximising_player and value >= best_move) or (not is_maximising_player and value <= best_move):
      best_move = value
      best_move_found = move

  return best_move_found