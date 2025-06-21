import numpy as np
from .Color import Color
from .Position import Position


class Face:
    _content = np.array([])

    def __init__(self, color: Color) -> None:
        self.content = np.full((3, 3), color, dtype=str)

    def __str__(self):
        return str(self.content)

    def __getitem__(self, key):
        return self.content[key]

    def __setitem__(self, key, value):
        self.content[key] = value


class Rubik:
    _front = Face(Color.WHITE)
    _back = Face(Color.YELLOW)

    _top = Face(Color.RED)
    _bottom = Face(Color.ORANGE)

    _right = Face(Color.BLUE)
    _left = Face(Color.GREEN)

    def __init__(self, mix: str) -> None:
        pass

    def rotate(self, position: Position) -> None:
        pass

    def counter_rotate(self, position: Position) -> None:
        pass

    def double_rotate(self, position: Position) -> None:
        pass