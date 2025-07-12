from functools import lru_cache
from typing import NamedTuple

from .Position import Position


class MoveForFace(NamedTuple):
    up:     Position
    down:   Position
    front:  Position
    back:   Position
    left:   Position
    right:  Position


class Moves(NamedTuple):
    UP:     MoveForFace
    DOWN:   MoveForFace
    FRONT:  MoveForFace
    BACK:   MoveForFace
    LEFT:   MoveForFace
    RIGHT:  MoveForFace


@lru_cache(maxsize=1)
def get_moves():
    return Moves(
        UP=MoveForFace(
            up=Position.BACK,
            down=Position.FRONT,
            front=Position.UP,
            back=Position.DOWN,
            left=Position.LEFT,
            right=Position.RIGHT,
        ),
        DOWN=MoveForFace(
            up=Position.FRONT,
            down=Position.BACK,
            front=Position.DOWN,
            back=Position.UP,
            left=Position.LEFT,
            right=Position.RIGHT,
        ),
        FRONT=MoveForFace(
            up=Position.UP,
            down=Position.DOWN,
            front=Position.FRONT,
            back=Position.BACK,
            left=Position.LEFT,
            right=Position.RIGHT,
        ),
        BACK=MoveForFace(
            up=Position.UP,
            down=Position.DOWN,
            front=Position.BACK,
            back=Position.FRONT,
            left=Position.RIGHT,
            right=Position.LEFT,
        ),
        LEFT=MoveForFace(
            up=Position.UP,
            down=Position.DOWN,
            front=Position.LEFT,
            back=Position.RIGHT,
            left=Position.BACK,
            right=Position.FRONT,
        ),
        RIGHT=MoveForFace(
            up=Position.UP,
            down=Position.DOWN,
            front=Position.RIGHT,
            back=Position.LEFT,
            left=Position.FRONT,
            right=Position.BACK,
        ),
    )
