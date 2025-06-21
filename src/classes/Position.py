from enum import Enum


class Position(Enum):
    TOP = 'U'
    BOTTOM = 'D'
    RIGHT = 'R'
    LEFT = 'L'
    FRONT = 'F'
    BACK = 'B'

    def __str__(self):
        return self.value

    def __eq__(self, other: object | str) -> bool:
        if isinstance(other, Position):
            return super().__eq__(other)
        if isinstance(other, str):
            return self.value == other or self.value == other.lower()
        return False