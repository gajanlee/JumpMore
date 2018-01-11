from func import *

def distance(*points):
    points = points[0]
    piece_x, piece_y = points[0], points[1]
    board_x, board_y = points[2], points[3]
    print(piece_x, piece_y, board_x, board_y)
    return math.sqrt( abs(piece_x - board_x) ** 2 + abs(piece_y - board_y) )

