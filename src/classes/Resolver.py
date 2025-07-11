import logging
from .Position import Position, PRIME , DOUBLE
from .Rubik import Rubik


class Resolver:
    def __init__(self, rubik: Rubik):
        self.rubik = rubik
        logging.info('STEP 1')
        self.up_cross()
        logging.info('STEP 2')
        self.up_corners()

    def up_cross(self):
        order = [self.rubik.front[1, 1], self.rubik.right[1, 1], self.rubik.back[1, 1], self.rubik.left[1, 1]]
        for i in range(len(order)):
            self.search_edges_for_up_cross([self.rubik.up[1, 1], order[i]])
            if self.rubik.front[0, 1] != order[i]:
                self.do_moves([
                    Position.FRONT.counter_clockwise(),
                    Position.UP.clockwise(),
                    Position.LEFT.counter_clockwise(),
                    Position.UP.counter_clockwise(),
                ])
            self.do_moves([
                Position.UP.clockwise(),
            ])

    def search_edges_for_up_cross(self, colors: list[str]):
        if self.rubik.up[2, 1] in colors and self.rubik.front[0, 1] in colors:
            return
        elif self.rubik.up[1, 2] in colors and self.rubik.right[0, 1] in colors:
            self.do_moves([
                Position.RIGHT.double_clockwise(),
                Position.DOWN.counter_clockwise(),
                Position.FRONT.double_clockwise(),
            ])
        elif self.rubik.up[1, 0] in colors and self.rubik.left[0, 1] in colors:
            self.do_moves([
                  Position.LEFT.double_clockwise(),
                  Position.DOWN.clockwise(),
                  Position.FRONT.double_clockwise(),
            ])
        elif self.rubik.up[0, 1] in colors and self.rubik.back[0, 1] in colors:
            self.do_moves([
                Position.BACK.double_clockwise(),
                Position.DOWN.double_clockwise(),
                Position.FRONT.double_clockwise(),
            ])
        elif self.rubik.down[0, 1] in colors and self.rubik.front[2, 1] in colors:
            self.do_moves([
                Position.FRONT.double_clockwise(),
            ])
        elif self.rubik.down[1, 2] in colors and self.rubik.right[2, 1] in colors:
            self.do_moves([
                Position.DOWN.counter_clockwise(),
                Position.FRONT.double_clockwise(),
            ])
        elif self.rubik.down[1, 0] in colors and self.rubik.left[2, 1] in colors:
            self.do_moves([
                Position.DOWN.clockwise(),
                Position.FRONT.double_clockwise(),
            ])
        elif self.rubik.down[2, 1] in colors and self.rubik.back[2, 1] in colors:
            self.do_moves([
                Position.DOWN.double_clockwise(),
                Position.FRONT.double_clockwise(),
            ])
        elif self.rubik.front[1, 0] in colors and self.rubik.left[1, 2] in colors:
            self.do_moves([
                Position.FRONT.clockwise(),
            ])
        elif self.rubik.front[1, 2] in colors and self.rubik.right[1, 0] in colors:
            self.do_moves([
                Position.FRONT.counter_clockwise(),
            ])
        elif self.rubik.back[1, 2] in colors and self.rubik.right[1, 2] in colors:
            self.do_moves([
                Position.BACK.counter_clockwise(),
                Position.DOWN.double_clockwise(),
                Position.BACK.clockwise(),
                Position.FRONT.double_clockwise(),
            ])
        elif self.rubik.back[1, 0] in colors and self.rubik.left[1, 0] in colors:
            self.do_moves([
                Position.BACK.clockwise(),
                Position.DOWN.double_clockwise(),
                Position.BACK.counter_clockwise(),
                Position.FRONT.double_clockwise(),
            ])
        else:
            raise "PROBLEM UP CROSS"

    def up_corners(self):
        order = [self.rubik.front[1, 1], self.rubik.right[1, 1], self.rubik.back[1, 1], self.rubik.left[1, 1]]
        for i in range(len(order)):
            self.search_corner_for_up([self.rubik.up[1, 1], order[i], order[i - 1]])
            self.good_orientation_for_corner([self.rubik.up[1, 1], order[i], order[i - 1]])
            self.do_moves([
                Position.UP.clockwise(),
            ])

    def search_corner_for_up(self, colors: list[str]):
        if self.rubik.up[2, 0] in colors and self.rubik.front[0, 0] in colors and self.rubik.left[0, 2] in colors:
            return
        elif self.rubik.up[2, 2] in colors and self.rubik.front[0, 2] in colors and self.rubik.right[0, 0] in colors:
            self.do_moves([
                Position.LEFT.clockwise(),
                Position.RIGHT.counter_clockwise(),
                Position.DOWN.counter_clockwise(),
                Position.LEFT.counter_clockwise(),
                Position.RIGHT.clockwise(),
            ])
        elif self.rubik.up[0, 0] in colors and self.rubik.back[0, 0] in colors and self.rubik.left[0, 0] in colors:
            self.do_moves([
                Position.LEFT.counter_clockwise(),
                Position.DOWN.double_clockwise(),
                Position.LEFT.double_clockwise(),
                Position.DOWN.counter_clockwise(),
                Position.LEFT.counter_clockwise(),
            ])
        elif self.rubik.up[0, 2] in colors and self.rubik.back[0, 2] in colors and self.rubik.right[0, 2] in colors:
            self.do_moves([
                Position.LEFT.clockwise(),
                Position.RIGHT.clockwise(),
                Position.DOWN.double_clockwise(),
                Position.LEFT.counter_clockwise(),
                Position.RIGHT.counter_clockwise(),
            ])
        elif self.rubik.down[0, 0] in colors and self.rubik.front[2, 0] in colors and self.rubik.left[2, 2] in colors:
            self.do_moves([
                Position.DOWN.clockwise(),
                Position.LEFT.clockwise(),
                Position.DOWN.counter_clockwise(),
                Position.LEFT.counter_clockwise(),
            ])
        elif self.rubik.down[0, 2] in colors and self.rubik.front[2, 2] in colors and \
                self.rubik.right[2, 0] in colors:
            self.do_moves([
                Position.LEFT.clockwise(),
                Position.DOWN.counter_clockwise(),
                Position.LEFT.counter_clockwise(),
            ])
        elif self.rubik.down[2, 2] in colors and self.rubik.back[2, 2] in colors and self.rubik.right[2, 2] in colors:
            self.do_moves([
                Position.LEFT.clockwise(),
                Position.DOWN.double_clockwise(),
                Position.LEFT.counter_clockwise(),
            ])
        elif self.rubik.down[2, 0] in colors and self.rubik.back[2, 0] in colors and self.rubik.left[2, 0] in colors:
            self.do_moves([
                Position.DOWN.counter_clockwise(),
                Position.LEFT.clockwise(),
                Position.DOWN.double_clockwise(),
                Position.LEFT.counter_clockwise(),
            ])
        else:
            raise "PROBLEM UP CORNER"

    def good_orientation_for_corner(self, colors):
        if self.rubik.up[2, 0] == colors[0]:
            return
        elif self.rubik.up[2, 0] == colors[1]:
            self.do_moves([
                Position.LEFT.clockwise(),
                Position.DOWN.clockwise(),
                Position.LEFT.counter_clockwise(),
                Position.DOWN.counter_clockwise(),
                Position.LEFT.clockwise(),
                Position.DOWN.clockwise(),
                Position.LEFT.counter_clockwise(),
                Position.DOWN.counter_clockwise(),
            ])
        else:
            self.do_moves([
                Position.FRONT.counter_clockwise(),
                Position.DOWN.counter_clockwise(),
                Position.FRONT.clockwise(),
                Position.DOWN.clockwise(),
                Position.FRONT.counter_clockwise(),
                Position.DOWN.counter_clockwise(),
                Position.FRONT.clockwise(),
                Position.DOWN.clockwise(),
            ])

    def belgian_story(self, left=False):
        if left:
            self.do_moves([
                Position.DOWN.clockwise(),
                Position.LEFT.counter_clockwise(),
                Position.DOWN.counter_clockwise(),
                Position.LEFT.clockwise(),
                Position.DOWN.counter_clockwise(),
                Position.FRONT.counter_clockwise(),
                Position.DOWN.clockwise(),
                Position.FRONT.clockwise(),
            ])
        else:
            self.do_moves([
                Position.DOWN.counter_clockwise(),
                Position.RIGHT.counter_clockwise(),
                Position.DOWN.clockwise(),
                Position.RIGHT.clockwise(),
                Position.DOWN.clockwise(),
                Position.FRONT.clockwise(),
                Position.DOWN.counter_clockwise(),
                Position.FRONT.counter_clockwise(),
            ])

    def do_moves(self, moves: list[str]):
        for move in moves:
            modifier = move[1] if len(move) == 2 else ""
            if modifier in PRIME:
                self.rubik.counter_clockwise_rotate(Position.get_good_position(move[0]))
            elif modifier is DOUBLE:
                self.rubik.double_clockwise_rotate(Position.get_good_position(move[0]))
            else:
                self.rubik.clockwise_rotate(Position.get_good_position(move[0]))
        self.rubik.solution.extend(moves)
