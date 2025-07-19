import logging
from .Position import Position, PRIME , DOUBLE
from .Rubik import Rubik
from .Move import MoveForFace, get_moves
from .Color import get_colors_faces
import numpy as np


class Resolver:
    def __init__(self, rubik: Rubik):
        logging.info("Start resolving")

        self.rubik = rubik
        logging.info("STEP 1")
        self.up_cross()

        logging.info("STEP 2")
        self.up_corners()

        logging.info("STEP 3")
        self.second_line()

        logging.info("Resolved")

    def up_cross(self):
        order = [
            self.rubik.front.get_color(),
            self.rubik.right.get_color(),
            self.rubik.back.get_color(),
            self.rubik.left.get_color(),
        ]
        for i in range(len(order)):
            self.search_edges_for_up_cross([self.rubik.up.get_color(), order[i]])
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
        order = [
            self.rubik.front.get_color(),
            self.rubik.right.get_color(),
            self.rubik.back.get_color(),
            self.rubik.left.get_color(),
        ]
        for i in range(len(order)):
            self.search_corner_for_up([self.rubik.up.get_color(), order[i], order[i - 1]])
            self.good_orientation_for_corner([self.rubik.up.get_color(), order[i], order[i - 1]])
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

    def second_line(self):
        colors = [
            self.rubik.front.get_color(),
            self.rubik.right.get_color(),
            self.rubik.back.get_color(),
            self.rubik.left.get_color(),
        ]
        for _ in range(len(colors)):
            self.search_edges_for_second_line(colors)
        if not self.check_second_line_good():
            for _ in range(len(colors)):
                self.search_edges_for_second_line(colors)

    def search_edges_for_second_line(self, colors: list[str]):
        if self.rubik.front[2, 1] in colors and self.rubik.down[0, 1] in colors:
            if self.rubik.front[2, 1] is get_colors_faces().FRONT.front:
                if self.rubik.down[0, 1] is get_colors_faces().FRONT.left:
                    self.belgian_story(get_moves().FRONT, Position.LEFT)
                elif self.rubik.down[0, 1] is get_colors_faces().FRONT.right:
                    self.belgian_story(get_moves().FRONT, Position.RIGHT)
            elif self.rubik.front[2, 1] is get_colors_faces().FRONT.right:
                self.do_moves([Position.DOWN.clockwise()])
                if self.rubik.down[1, 2] is get_colors_faces().FRONT.front:
                    self.belgian_story(get_moves().RIGHT, Position.LEFT)
                elif self.rubik.down[1, 2] is get_colors_faces().FRONT.back:
                    self.belgian_story(get_moves().RIGHT, Position.RIGHT)
            elif self.rubik.front[2, 1] is get_colors_faces().FRONT.back:
                self.do_moves([Position.DOWN.double_clockwise()])
                if self.rubik.down[2, 1] is get_colors_faces().FRONT.right:
                    self.belgian_story(get_moves().BACK, Position.LEFT)
                elif self.rubik.down[2, 1] is get_colors_faces().FRONT.left:
                    self.belgian_story(get_moves().BACK, Position.RIGHT)
            elif self.rubik.front[2, 1] is get_colors_faces().FRONT.left:
                self.do_moves([Position.DOWN.counter_clockwise()])
                if self.rubik.down[1, 0] is get_colors_faces().FRONT.back:
                    self.belgian_story(get_moves().LEFT, Position.LEFT)
                elif self.rubik.down[1, 0] is get_colors_faces().FRONT.front:
                    self.belgian_story(get_moves().LEFT, Position.RIGHT)
        elif self.rubik.right[2, 1] in colors and self.rubik.down[1, 2] in colors:
            if self.rubik.right[2, 1] is get_colors_faces().RIGHT.front:
                if self.rubik.down[1, 2] is get_colors_faces().RIGHT.left:
                    self.belgian_story(get_moves().RIGHT, Position.LEFT)
                elif self.rubik.down[1, 2] is get_colors_faces().RIGHT.right:
                    self.belgian_story(get_moves().RIGHT, Position.RIGHT)
            elif self.rubik.right[2, 1] is get_colors_faces().RIGHT.right:
                self.do_moves([Position.DOWN.clockwise()])
                if self.rubik.down[2, 1] is get_colors_faces().RIGHT.front:
                    self.belgian_story(get_moves().BACK, Position.LEFT)
                elif self.rubik.down[2, 1] is get_colors_faces().RIGHT.back:
                    self.belgian_story(get_moves().BACK, Position.RIGHT)
            elif self.rubik.right[2, 1] is get_colors_faces().RIGHT.back:
                self.do_moves([Position.DOWN.double_clockwise()])
                if self.rubik.down[1, 0] is get_colors_faces().RIGHT.right:
                    self.belgian_story(get_moves().LEFT, Position.LEFT)
                elif self.rubik.down[1, 0] is get_colors_faces().RIGHT.left:
                    self.belgian_story(get_moves().LEFT, Position.RIGHT)
            elif self.rubik.right[2, 1] is get_colors_faces().RIGHT.left:
                self.do_moves([Position.DOWN.counter_clockwise()])
                if self.rubik.down[0, 1] is get_colors_faces().RIGHT.back:
                    self.belgian_story(get_moves().FRONT, Position.LEFT)
                elif self.rubik.down[0, 1] is get_colors_faces().RIGHT.front:
                    self.belgian_story(get_moves().FRONT, Position.RIGHT)
        elif self.rubik.back[2, 1] in colors and self.rubik.down[2, 1] in colors:
            if self.rubik.back[2, 1] is get_colors_faces().BACK.front:
                if self.rubik.down[2, 1] is get_colors_faces().BACK.left:
                    self.belgian_story(get_moves().BACK, Position.LEFT)
                elif self.rubik.down[2, 1] is get_colors_faces().BACK.right:
                    self.belgian_story(get_moves().BACK, Position.RIGHT)
            elif self.rubik.back[2, 1] is get_colors_faces().BACK.right:
                self.do_moves([Position.DOWN.clockwise()])
                if self.rubik.down[1, 0] is get_colors_faces().BACK.front:
                    self.belgian_story(get_moves().LEFT, Position.LEFT)
                elif self.rubik.down[1, 0] is get_colors_faces().BACK.back:
                    self.belgian_story(get_moves().LEFT, Position.RIGHT)
            elif self.rubik.back[2, 1] is get_colors_faces().BACK.back:
                self.do_moves([Position.DOWN.double_clockwise()])
                if self.rubik.down[0, 1] is get_colors_faces().BACK.right:
                    self.belgian_story(get_moves().FRONT, Position.LEFT)
                elif self.rubik.down[0, 1] is get_colors_faces().BACK.left:
                    self.belgian_story(get_moves().FRONT, Position.RIGHT)
            elif self.rubik.back[2, 1] is get_colors_faces().BACK.left:
                self.do_moves([Position.DOWN.counter_clockwise()])
                if self.rubik.down[1, 2] is get_colors_faces().BACK.back:
                    self.belgian_story(get_moves().RIGHT, Position.LEFT)
                elif self.rubik.down[1, 2] is get_colors_faces().BACK.front:
                    self.belgian_story(get_moves().RIGHT, Position.RIGHT)
        elif self.rubik.left[2, 1] in colors and self.rubik.down[1, 0] in colors:
            if self.rubik.left[2, 1] is get_colors_faces().LEFT.front:
                if self.rubik.down[1, 0] is get_colors_faces().LEFT.left:
                    self.belgian_story(get_moves().LEFT, Position.LEFT)
                elif self.rubik.down[1, 0] is get_colors_faces().LEFT.right:
                    self.belgian_story(get_moves().LEFT, Position.RIGHT)
            elif self.rubik.left[2, 1] is get_colors_faces().LEFT.right:
                self.do_moves([Position.DOWN.clockwise()])
                if self.rubik.down[0, 1] is get_colors_faces().LEFT.front:
                    self.belgian_story(get_moves().FRONT, Position.LEFT)
                elif self.rubik.down[0, 1] is get_colors_faces().LEFT.back:
                    self.belgian_story(get_moves().FRONT, Position.RIGHT)
            elif self.rubik.left[2, 1] is get_colors_faces().LEFT.back:
                self.do_moves([Position.DOWN.double_clockwise()])
                if self.rubik.down[1, 2] is get_colors_faces().LEFT.right:
                    self.belgian_story(get_moves().RIGHT, Position.LEFT)
                elif self.rubik.down[1, 2] is get_colors_faces().LEFT.left:
                    self.belgian_story(get_moves().RIGHT, Position.RIGHT)
            elif self.rubik.left[2, 1] is get_colors_faces().LEFT.left:
                self.do_moves([Position.DOWN.counter_clockwise()])
                if self.rubik.down[2, 1] is get_colors_faces().LEFT.back:
                    self.belgian_story(get_moves().BACK, Position.LEFT)
                elif self.rubik.down[2, 1] is get_colors_faces().LEFT.front:
                    self.belgian_story(get_moves().BACK, Position.RIGHT)

    def check_second_line_good(self):
        if self.rubik.front[1, 0] is not get_colors_faces().FRONT.front:
            self.belgian_story(get_moves().FRONT, Position.LEFT)
            return False
        elif self.rubik.right[1, 0] is not get_colors_faces().FRONT.right:
            self.belgian_story(get_moves().RIGHT, Position.LEFT)
            return False
        elif self.rubik.back[1, 2] is not get_colors_faces().FRONT.back:
            self.belgian_story(get_moves().BACK, Position.LEFT)
            return False
        elif self.rubik.left[1, 0] is not get_colors_faces().FRONT.left:
            self.belgian_story(get_moves().LEFT, Position.LEFT)
            return False
        return True

    def belgian_story(self, face : MoveForFace, direction : Position):
        if direction == Position.LEFT:
            self.do_moves([
                face.down.clockwise(),
                face.left.clockwise(),
                face.down.counter_clockwise(),
                face.left.counter_clockwise(),
                face.down.counter_clockwise(),
                face.front.counter_clockwise(),
                face.down.clockwise(),
                face.front.clockwise(),
            ])
        elif direction == Position.RIGHT:
            self.do_moves([
                face.down.counter_clockwise(),
                face.right.counter_clockwise(),
                face.down.clockwise(),
                face.right.clockwise(),
                face.down.clockwise(),
                face.front.clockwise(),
                face.down.counter_clockwise(),
                face.front.counter_clockwise(),
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
        self.rubik.solution = np.append(self.rubik.solution, moves)
