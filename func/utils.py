from func import *

def distance(*points):
    piece_x, piece_y = points[0], points[1]
    board_x, board_y = points[0], points[1]
    return math.sqrt( abs(piece_x - board_y) ** 2 + abs(piece_y - board_y) )

