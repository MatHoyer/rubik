import logging
from .Position import Position
from .Rubik import Rubik


class Resolver:
    def __init__(self, rubik: Rubik):
        self.rubik = rubik
        logging.info('STEP 1')
        self.top_cross()
        logging.info('STEP 2')
        self.top_corners()

    def top_cross(self):
        order = [self.rubik.front[1, 1], self.rubik.right[1, 1], self.rubik.back[1, 1], self.rubik.left[1, 1]]
        for i in range(len(order)):
            self.search_edges_for_top_cross([self.rubik.top[1, 1], order[i]])
            if self.rubik.front[0, 1] != order[i]:
                self.do_moves(["F'", "U", "L'", "U'"])
            self.do_moves(["U"])

    def search_edges_for_top_cross(self, colors: list[str]):
        if self.rubik.top[2, 1] in colors and self.rubik.front[0, 1] in colors:
            return
        elif self.rubik.top[1, 2] in colors and self.rubik.right[0, 1] in colors:
            self.do_moves(["R2", "D'", "F2"])
        elif self.rubik.top[1, 0] in colors and self.rubik.left[0, 1] in colors:
            self.do_moves(["L2", "D", "F2"])
        elif self.rubik.top[0, 1] in colors and self.rubik.back[0, 1] in colors:
            self.do_moves(["B2", "D2", "F2"])
        elif self.rubik.bottom[0, 1] in colors and self.rubik.front[2, 1] in colors:
            self.do_moves(["F2"])
        elif self.rubik.bottom[1, 2] in colors and self.rubik.right[2, 1] in colors:
            self.do_moves(["D'", "F2"])
        elif self.rubik.bottom[1, 0] in colors and self.rubik.left[2, 1] in colors:
            self.do_moves(["D", "F2"])
        elif self.rubik.bottom[2, 1] in colors and self.rubik.back[2, 1] in colors:
            self.do_moves(["D2", "F2"])
        elif self.rubik.front[1, 0] in colors and self.rubik.left[1, 2] in colors:
            self.do_moves(["F"])
        elif self.rubik.front[1, 2] in colors and self.rubik.right[1, 0] in colors:
            self.do_moves(["F'"])
        elif self.rubik.back[1, 2] in colors and self.rubik.right[1, 2] in colors:
            self.do_moves(["B'", "D2", "B", "F2"])
        elif self.rubik.back[1, 0] in colors and self.rubik.left[1, 0] in colors:
            self.do_moves(["B", "D2", "B'", "F2"])
        else:
            raise "PROBLEM TOP CROSS"

    def top_corners(self):
        order = [self.rubik.front[1, 1], self.rubik.right[1, 1], self.rubik.back[1, 1], self.rubik.left[1, 1]]
        for i in range(len(order)):
            self.search_corner_for_top([self.rubik.top[1, 1], order[i], order[i - 1]])
            self.good_orientation_for_corner([self.rubik.top[1, 1], order[i], order[i - 1]])
            self.do_moves(["U"])

    def search_corner_for_top(self, colors: list[str]):
        if self.rubik.top[2, 0] in colors and self.rubik.front[0, 0] in colors and self.rubik.left[0, 2] in colors:
            return
        elif self.rubik.top[2, 2] in colors and self.rubik.front[0, 2] in colors and self.rubik.right[0, 0] in colors:
            self.do_moves(["L", "R'", "D'", "L'", "R"])
        elif self.rubik.top[0, 0] in colors and self.rubik.back[0, 0] in colors and self.rubik.left[0, 0] in colors:
            self.do_moves(["L'", "D2", "L2", "D'", "L'"])
        elif self.rubik.top[0, 2] in colors and self.rubik.back[0, 2] in colors and self.rubik.right[0, 2] in colors:
            self.do_moves(["L", "R", "D2", "L'", "R'"])
        elif self.rubik.bottom[0, 0] in colors and self.rubik.front[2, 0] in colors and self.rubik.left[2, 2] in colors:
            self.do_moves(["D", "L", "D'", "L'"])
        elif self.rubik.bottom[0, 2] in colors and self.rubik.front[2, 2] in colors and \
                self.rubik.right[2, 0] in colors:
            self.do_moves(["L", "D'", "L'"])
        elif self.rubik.bottom[2, 2] in colors and self.rubik.back[2, 2] in colors and self.rubik.right[2, 2] in colors:
            self.do_moves(["L", "D2", "L'"])
        elif self.rubik.bottom[2, 0] in colors and self.rubik.back[2, 0] in colors and self.rubik.left[2, 0] in colors:
            self.do_moves(["D'", "L", "D2", "L'"])
        else:
            raise "PROBLEM TOP CORNER"

    def good_orientation_for_corner(self, colors):
        if self.rubik.top[2, 0] == colors[0]:
            return
        elif self.rubik.top[2, 0] == colors[1]:
            self.do_moves(["L", "D", "L'", "D'", "L", "D", "L'", "D'"])
        else:
            self.do_moves(["F'", "D'", "F", "D", "F'", "D'", "F", "D"])

    def belgian_story(self, left=False):
        if left:
            self.do_moves(["D", "L'", "D'", "L", "D'", "F'", "D", "F"])
        else:
            self.do_moves(["D'", "R'", "D", "R", "D", "F", "D'", "F'"])

    def do_moves(self, moves: list[str]):
        for move in moves:
            position_dict = {
                "F": Position.FRONT,
                "B": Position.BACK,
                "U": Position.TOP,
                "D": Position.BOTTOM,
                "L": Position.LEFT,
                "R": Position.RIGHT,
            }
            modifier = move[1] if len(move) == 2 else ""
            if modifier == "'":
                self.rubik.counter_rotate(position_dict[move[0]])
            elif modifier == "2":
                self.rubik.double_rotate(position_dict[move[0]])
            else:
                self.rubik.rotate(position_dict[move[0]])
        self.rubik.solution.extend(moves)
