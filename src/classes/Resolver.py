import logging
from .Position import Position, PRIME , DOUBLE
from .Rubik import Rubik
import numpy as np


class Resolver:
    def __init__(self, rubik: Rubik):
        self.rubik = rubik
        logging.info("Start resolving")

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
