import chess
import tables
import attackedSquares

def eval(board: chess.Board):
    if board.is_checkmate():
        return -99999 if board.turn == chess.WHITE else 99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    
    #
    # TODO - Add scoring for check
    # TODO - Add scoring for controlling squares (More than opponent, prioritise centre) <--- Work on this now
    #

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = tables.pieceValues[piece.piece_type]
            if piece.color == chess.WHITE:
                sqaureValue = tables.blendTables(piece.piece_type, True, board)[square]
                score += value
                score += sqaureValue
            else:
                sqaureValue = tables.blendTables(piece.piece_type, False, board)[square]
                score -= value
                score -= sqaureValue

    score += board.is_check()*-20 if board.turn == chess.WHITE else board.is_check()*20

    # TODO - Make dependent on some sort of mask that values centre and opponent's side more
    # Encourage attacking more squares
    score += len(attackedSquares.attacked_squares(board, color=chess.WHITE))*15
    score -= len(attackedSquares.attacked_squares(board, color=chess.BLACK))*15

    #Dependent on colour
    colorConditionsScore = 0

    colorConditionsScore = -(board.occupied.bit_count() * 10)

    if board.move_stack:
        lastMove = board.peek()
        movedPiece = board.piece_at(lastMove.to_square)
        if (board.fullmove_number <= 8 and movedPiece is not None and movedPiece.piece_type == chess.ROOK):
            colorConditionsScore -= 200 - 25 * board.fullmove_number


    colorConditionsScore += board.is_check()*20
              
    if board.turn == chess.BLACK:
        score += colorConditionsScore
    else:
        score -= colorConditionsScore
                
    return score