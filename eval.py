import chess
import tables

def eval(board):
    if board.is_checkmate():
        return -99999 if board.turn == chess.WHITE else 99999
    if board.is_stalemate() or board.is_insufficient_material() or board.can_claim_draw():
        return 0
    
    #
    # TODO - Add scoring for check
    # TODO - Add scoring for controlling squares (More than opponent, prioritise centre)
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
                
    if board.turn == chess.WHITE:
      score -= board.occupied.bit_count()*10
    else:
      score += board.occupied.bit_count()*10
                
    return score