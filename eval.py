import chess
import tables

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

    otherConditionsScore = 0
    otherConditionsScore -= board.occupied.bit_count()*10
    otherConditionsScore += board.has_castling_rights(color=board.turn)*30
    otherConditionsScore += board.is_check()*20
              
    if board.turn == chess.WHITE:
        score += otherConditionsScore
    else:
        score -= otherConditionsScore
                
    return score