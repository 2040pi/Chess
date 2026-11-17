import chess
import eval
import preorderMoves

def minimax(depth, board, alpha, beta, is_maximising_player):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -1000000 + depth
        return 1000000 - depth

    if board.is_game_over():
        return 0

    if depth == 0:
        return eval.eval(board)

    legal_moves = preorderMoves.orderedMoves(board)
    if not legal_moves:
        return 0

    if is_maximising_player:
        best_score = -1000000
        for move in legal_moves:
            board.push(move)
            score = minimax(
                depth - 1,
                board,
                alpha,
                beta,
                False,
            )
            board.pop()

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = 1000000
        for move in legal_moves:
            board.push(move)
            score = minimax(
                depth - 1,
                board,
                alpha,
                beta,
                True,
            )
            board.pop()

            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score


def minimax_root(depth, board, is_maximising_player=True):
    legal_moves = preorderMoves.orderedMoves(board)
    if not legal_moves:
        return None

    best_score = -1000000 if is_maximising_player else 1000000
    best_move = None

    for move in legal_moves:
        board.push(move)

        if board.is_checkmate():
            board.pop()
            return move

        score = minimax(
            depth - 1,
            board,
            -1000000,
            1000000,
            not is_maximising_player,
        )
        board.pop()

        if (
            is_maximising_player
            and score > best_score
        ) or (
            not is_maximising_player
            and score < best_score
        ):
            best_score = score
            best_move = move

    return best_move