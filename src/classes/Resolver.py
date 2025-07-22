import logging
from .Position import Position, PRIME , DOUBLE
from .Rubik import Rubik
import numpy as np
from .Color import get_colors


class Resolver:
    def __init__(self, rubik: Rubik):
        self.rubik = rubik
        logging.info("Start resolving")
        self.set_up_2x2x3()
        if not self.check_nb_of_colors_is_good():
            logging.info("BAD !!!!!!!!!!!!!!!")
            logging.info("BAD !!!!!!!!!!!!!!!")
            logging.info("BAD !!!!!!!!!!!!!!!")
            logging.info("BAD !!!!!!!!!!!!!!!")
            logging.info("BAD !!!!!!!!!!!!!!!")

    def check_nb_of_colors_is_good(self):
        colors = {
            get_colors().BLUE: 0,
            get_colors().ORANGE: 0,
            get_colors().GREEN: 0,
            get_colors().RED: 0,
            get_colors().YELLOW: 0,
            get_colors().WHITE: 0,
        }
        faces = [
            self.rubik.front,
            self.rubik.back,
            self.rubik.up,
            self.rubik.down,
            self.rubik.left,
            self.rubik.right
        ]
        for face in faces:
            for i in range(3):
                for j in range(3):
                    colors[face[i, j]] += 1
        for color in colors.values():
            if color != 9:
                return False
        return True

    def set_up_2x2x3(self):
        self.change_corner_colors(self.rubik.front, [0, 0], self.rubik.up, [2, 0], self.rubik.left, [0, 2])
        self.change_corner_colors(self.rubik.front, [0, 2], self.rubik.up, [2, 2], self.rubik.right, [0, 0])
        self.change_corner_colors(self.rubik.front, [2, 0], self.rubik.down, [0, 0], self.rubik.left, [2, 2])
        self.change_corner_colors(self.rubik.front, [2, 2], self.rubik.down, [0, 2], self.rubik.right, [2, 0])

        self.change_corner_colors(self.rubik.back, [0, 0], self.rubik.up, [0, 0], self.rubik.left, [0, 0])
        self.change_corner_colors(self.rubik.back, [0, 2], self.rubik.up, [0, 2], self.rubik.right, [0, 2])
        self.change_corner_colors(self.rubik.back, [2, 0], self.rubik.down, [2, 0], self.rubik.left, [2, 0])
        self.change_corner_colors(self.rubik.back, [2, 2], self.rubik.down, [2, 2], self.rubik.right, [2, 2])

        self.rubik.left.set_color(2, 0, get_colors().ORANGE)
        self.rubik.back.set_color(2, 0, get_colors().BLUE)
        self.rubik.down.set_color(2, 0, get_colors().YELLOW)

        self.rubik.right.set_color(2, 2, get_colors().RED)
        self.rubik.back.set_color(2, 2, get_colors().BLUE)
        self.rubik.down.set_color(2, 2, get_colors().YELLOW)

        self.change_edge_colors(self.rubik.up, [2, 1], self.rubik.front, [0, 1])
        self.change_edge_colors(self.rubik.up, [1, 0], self.rubik.left, [0, 1])
        self.change_edge_colors(self.rubik.up, [0, 1], self.rubik.back, [0, 1])
        self.change_edge_colors(self.rubik.up, [1, 2], self.rubik.right, [0, 1])

        self.change_edge_colors(self.rubik.down, [0, 1], self.rubik.front, [2, 1])
        self.change_edge_colors(self.rubik.down, [1, 0], self.rubik.left, [2, 1])
        self.change_edge_colors(self.rubik.down, [2, 1], self.rubik.back, [2, 1])
        self.change_edge_colors(self.rubik.down, [1, 2], self.rubik.right, [2, 1])

        self.change_edge_colors(self.rubik.front, [1, 0], self.rubik.left, [1, 2])
        self.change_edge_colors(self.rubik.front, [1, 2], self.rubik.right, [1, 0])

        self.change_edge_colors(self.rubik.back, [1, 0], self.rubik.left, [1, 0])
        self.change_edge_colors(self.rubik.back, [1, 2], self.rubik.right, [1, 2])

        self.rubik.left.set_color(1, 0, get_colors().ORANGE)
        self.rubik.left.set_color(2, 1, get_colors().ORANGE)

        self.rubik.right.set_color(2, 1, get_colors().RED)
        self.rubik.right.set_color(1, 2, get_colors().RED)

        self.rubik.back.set_color(1, 0, get_colors().BLUE)
        self.rubik.back.set_color(2, 1, get_colors().BLUE)
        self.rubik.back.set_color(1, 2, get_colors().BLUE)

        self.rubik.down.set_color(1, 0, get_colors().YELLOW)
        self.rubik.down.set_color(2, 1, get_colors().YELLOW)
        self.rubik.down.set_color(1, 2, get_colors().YELLOW)

    def change_corner_colors(self, pos_1, coord_1, pos_2, coord_2, pos_3, coord_3):
        left_corner_colors = [get_colors().ORANGE, get_colors().BLUE, get_colors().YELLOW]
        right_corner_colors = [get_colors().RED, get_colors().BLUE, get_colors().YELLOW]
        if (self.rubik.left[2, 0] not in left_corner_colors or
                self.rubik.down[2, 0] not in left_corner_colors or
                self.rubik.back[2, 0] not in left_corner_colors) and \
                pos_1[coord_1[0], coord_1[1]] in left_corner_colors and \
                pos_2[coord_2[0], coord_2[1]] in left_corner_colors and \
                pos_3[coord_3[0], coord_3[1]] in left_corner_colors:
            pos_1.set_color(coord_1[0], coord_1[1], self.rubik.left[2, 0])
            pos_2.set_color(coord_2[0], coord_2[1], self.rubik.down[2, 0])
            pos_3.set_color(coord_3[0], coord_3[1], self.rubik.back[2, 0])
            self.change_corner_colors(pos_1, coord_1, pos_2, coord_2, pos_3, coord_3)
        if (self.rubik.right[2, 2] not in right_corner_colors or
                self.rubik.down[2, 2] not in right_corner_colors or
                self.rubik.back[2, 2] not in right_corner_colors) and \
                pos_1[coord_1[0], coord_1[1]] in right_corner_colors and \
                pos_2[coord_2[0], coord_2[1]] in right_corner_colors and \
                pos_3[coord_3[0], coord_3[1]] in right_corner_colors:
            pos_1.set_color(coord_1[0], coord_1[1], self.rubik.right[2, 2])
            pos_2.set_color(coord_2[0], coord_2[1], self.rubik.down[2, 2])
            pos_3.set_color(coord_3[0], coord_3[1], self.rubik.back[2, 2])
            self.change_corner_colors(pos_1, coord_1, pos_2, coord_2, pos_3, coord_3)

    def change_edge_colors(self, pos_1, coord_1, pos_2, coord_2):
        colors_1 = [get_colors().ORANGE, get_colors().YELLOW]
        colors_2 = [get_colors().BLUE, get_colors().YELLOW]
        colors_3 = [get_colors().RED, get_colors().YELLOW]
        colors_4 = [get_colors().ORANGE, get_colors().BLUE]
        colors_5 = [get_colors().RED, get_colors().BLUE]
        if (self.rubik.left[2, 1] not in colors_1 or
                self.rubik.down[1, 0] not in colors_1) and \
                pos_1[coord_1[0], coord_1[1]] in colors_1 and \
                pos_2[coord_2[0], coord_2[1]] in colors_1:
            pos_1.set_color(coord_1[0], coord_1[1], self.rubik.left[2, 1])
            pos_2.set_color(coord_2[0], coord_2[1], self.rubik.down[1, 0])
            self.change_edge_colors(pos_1, coord_1, pos_2, coord_2)
        if (self.rubik.back[2, 1] not in colors_2 or
                self.rubik.down[2, 1] not in colors_2) and \
                pos_1[coord_1[0], coord_1[1]] in colors_2 and \
                pos_2[coord_2[0], coord_2[1]] in colors_2:
            pos_1.set_color(coord_1[0], coord_1[1], self.rubik.back[2, 1])
            pos_2.set_color(coord_2[0], coord_2[1], self.rubik.down[2, 1])
            self.change_edge_colors(pos_1, coord_1, pos_2, coord_2)
        if (self.rubik.right[2, 1] not in colors_3 or
                self.rubik.down[1, 2] not in colors_3) and \
                pos_1[coord_1[0], coord_1[1]] in colors_3 and \
                pos_2[coord_2[0], coord_2[1]] in colors_3:
            pos_1.set_color(coord_1[0], coord_1[1], self.rubik.right[2, 1])
            pos_2.set_color(coord_2[0], coord_2[1], self.rubik.down[1, 2])
            self.change_edge_colors(pos_1, coord_1, pos_2, coord_2)
        if (self.rubik.left[1, 0] not in colors_4 or
                self.rubik.back[1, 0] not in colors_4) and \
                pos_1[coord_1[0], coord_1[1]] in colors_4 and \
                pos_2[coord_2[0], coord_2[1]] in colors_4:
            pos_1.set_color(coord_1[0], coord_1[1], self.rubik.left[1, 0])
            pos_2.set_color(coord_2[0], coord_2[1], self.rubik.back[1, 0])
            self.change_edge_colors(pos_1, coord_1, pos_2, coord_2)
        if (self.rubik.right[1, 2] not in colors_5 or
                self.rubik.back[1, 2] not in colors_5) and \
                pos_1[coord_1[0], coord_1[1]] in colors_5 and \
                pos_2[coord_2[0], coord_2[1]] in colors_5:
            pos_1.set_color(coord_1[0], coord_1[1], self.rubik.right[1, 2])
            pos_2.set_color(coord_2[0], coord_2[1], self.rubik.back[1, 2])
            self.change_edge_colors(pos_1, coord_1, pos_2, coord_2)

    def do_moves(self, moves: list[str]):
        for move in moves:
            modifier = move[1] if len(move) == 2 else ""
            if modifier in PRIME:
                self.rubik.counter_clockwise_rotate(Position.get_good_position(move[0]))
            elif modifier is DOUBLE:
                self.rubik.double_clockwise_rotate(Position.get_good_position(move[0]))
            else:
                self.rubik.clockwise_rotate(Position.get_good_position(move[0]))
        self.rubik.solution = np.append(self.rubik.solution, moves)
