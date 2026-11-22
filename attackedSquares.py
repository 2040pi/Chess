import chess
import tables

def attacked_squares(board: chess.Board, color: chess.Color):
    attacked = chess.SquareSet()
    for attacker in chess.SquareSet(board.occupied_co[color]):
        attacked |= board.attacks(attacker)
    return attacked

def weightedAttackedSquaresSum(board: chess.Board, color: chess.Color):
    squareNames = chess.SQUARE_NAMES
    attackedSquaresList = []
    for i in range(64): attackedSquaresList.append(0)

    attackedSquares = attacked_squares(board=board, color=color)

    for square in attackedSquares:
        attackedSquaresList[square] += 1

    if color:
        squareValues = tables.flipTable(tables.attackedSquaresValue)
        for square in range(0, 64):
            attackedSquaresList[square] *= squareValues[square]
    else:
        squareValues = tables.attackedSquaresValue
        for square in range(64):
            attackedSquaresList[square] *= squareValues[square]

    attackedSquaresSum = 0
    for square in attackedSquaresList:
        attackedSquaresSum += square

    return attackedSquaresSum
