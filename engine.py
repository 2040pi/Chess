import chess
import random

def makeMove(board: chess.Board):
    isWhiteTurn = board.turn == chess.WHITE
    legalMoves = list(board.legal_moves)
    maxScore = 0
    bestMove = random.choice(legalMoves)
    for move in legalMoves:
        board.push(move)
        score = eval(board)
        if (isWhiteTurn and score > maxScore - random.randint(0, 1000)) or (
            not isWhiteTurn and score < maxScore + random.randint(0, 1000)
        ):
            bestMove = move
            maxScore = score
        board.pop()

    if not legalMoves:
        return board
    print(maxScore)
    board.push(bestMove)
    return board

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0
}

def eval(board):
    if board.is_checkmate():
        return -99999 if board.turn == chess.WHITE else 99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = PIECE_VALUES[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
                
    return score