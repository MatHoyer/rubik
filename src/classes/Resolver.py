from typing import TYPE_CHECKING
import logging
from .Position import Position

if TYPE_CHECKING:
    from .Rubik import Rubik


class Resolver:
    def __init__(self, rubik: "Rubik"):
        self.rubik = rubik
        logging.info('START RESOLVER')
        self.top_cross()

    def top_cross(self):
        order = [self.rubik.front[1, 1], self.rubik.right[1, 1], self.rubik.back[1, 1], self.rubik.left[1, 1]]
        for i in range(len(order)):
            self.search_edges([self.rubik.top[1, 1], order[i]])
            if self.rubik.front[0, 1] != order[i]:
                self.sliding_door()
            self.rubik.rotate(Position.TOP)
        pass

    def search_edges(self, colors: list[str]):
        if self.rubik.top[2, 1] in colors and self.rubik.front[0, 1] in colors:
            return
        elif self.rubik.top[1, 2] in colors and self.rubik.right[0, 1] in colors:
            self.rubik.double_rotate(Position.RIGHT)
            self.rubik.counter_rotate(Position.BOTTOM)
            self.rubik.double_rotate(Position.FRONT)
            self.rubik.solution.extend(["R2", "D'", "F2"])
        elif self.rubik.top[1, 0] in colors and self.rubik.left[0, 1] in colors:
            self.rubik.double_rotate(Position.LEFT)
            self.rubik.rotate(Position.BOTTOM)
            self.rubik.double_rotate(Position.FRONT)
            self.rubik.solution.extend(["L2", "D", "F2"])
        elif self.rubik.top[0, 1] in colors and self.rubik.back[0, 1] in colors:
            self.rubik.double_rotate(Position.BACK)
            self.rubik.double_rotate(Position.BOTTOM)
            self.rubik.double_rotate(Position.FRONT)
            self.rubik.solution.extend(["B2", "D2", "F2"])
        elif self.rubik.bottom[0, 1] in colors and self.rubik.front[2, 1] in colors:
            self.rubik.double_rotate(Position.FRONT)
            self.rubik.solution.extend(["F2"])
        elif self.rubik.bottom[1, 2] in colors and self.rubik.right[2, 1] in colors:
            self.rubik.counter_rotate(Position.BOTTOM)
            self.rubik.double_rotate(Position.FRONT)
            self.rubik.solution.extend(["D'", "F2"])
        elif self.rubik.bottom[1, 0] in colors and self.rubik.left[2, 1] in colors:
            self.rubik.rotate(Position.BOTTOM)
            self.rubik.double_rotate(Position.FRONT)
            self.rubik.solution.extend(["D", "F2"])
        elif self.rubik.bottom[2, 1] in colors and self.rubik.back[2, 1] in colors:
            self.rubik.double_rotate(Position.BOTTOM)
            self.rubik.double_rotate(Position.FRONT)
            self.rubik.solution.extend(["D2", "F2"])
        elif self.rubik.front[1, 0] in colors and self.rubik.left[1, 2] in colors:
            self.rubik.rotate(Position.FRONT)
            self.rubik.solution.extend(["F"])
        elif self.rubik.front[1, 2] in colors and self.rubik.right[1, 0] in colors:
            self.rubik.counter_rotate(Position.FRONT)
            self.rubik.solution.extend(["F'"])
        elif self.rubik.back[1, 2] in colors and self.rubik.right[1, 2] in colors:
            self.rubik.counter_rotate(Position.BACK)
            self.rubik.double_rotate(Position.BOTTOM)
            self.rubik.rotate(Position.BACK)
            self.rubik.double_rotate(Position.FRONT)
            self.rubik.solution.extend(["B'", "D2", "B", "F2"])
        elif self.rubik.back[1, 0] in colors and self.rubik.left[1, 0] in colors:
            self.rubik.rotate(Position.BACK)
            self.rubik.double_rotate(Position.BOTTOM)
            self.rubik.counter_rotate(Position.BACK)
            self.rubik.double_rotate(Position.FRONT)
            self.rubik.solution.extend(["B", "D2", "B'", "F2"])
        else:
            raise "PROBLEM TOP CROSS"

    def sliding_door(self):
        self.rubik.counter_rotate(Position.FRONT)
        self.rubik.rotate(Position.TOP)
        self.rubik.counter_rotate(Position.LEFT)
        self.rubik.counter_rotate(Position.TOP)
        self.rubik.solution.extend(["F'", "U", "L'", "U'"])

    def belgian_story(self, left=False):
        if left:
            self.rubik.rotate(Position.BOTTOM)
            self.rubik.counter_rotate(Position.LEFT)
            self.rubik.counter_rotate(Position.BOTTOM)
            self.rubik.rotate(Position.LEFT)
            self.rubik.counter_rotate(Position.BOTTOM)
            self.rubik.counter_rotate(Position.FRONT)
            self.rubik.rotate(Position.BOTTOM)
            self.rubik.rotate(Position.FRONT)
            self.rubik.solution.extend(["D", "L'", "D'", "L", "D'", "F'", "D", "F"])
        else:
            self.rubik.counter_rotate(Position.BOTTOM)
            self.rubik.counter_rotate(Position.RIGHT)
            self.rubik.rotate(Position.BOTTOM)
            self.rubik.rotate(Position.RIGHT)
            self.rubik.rotate(Position.BOTTOM)
            self.rubik.rotate(Position.FRONT)
            self.rubik.counter_rotate(Position.BOTTOM)
            self.rubik.counter_rotate(Position.FRONT)
            self.rubik.solution.extend(["D'", "R'", "D", "R", "D", "F", "D'", "F'"])
