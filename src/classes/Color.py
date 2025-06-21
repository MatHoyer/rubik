from enum import Enum


class Color(Enum):
    WHITE = 'W'
    YELLOW = 'Y'
    RED = 'R'
    ORANGE = 'O'
    BLUE = 'B'
    GREEN = 'G'

    def __str__(self):
        return self.value

    def __eq__(self, other: object | str) -> bool:
        if isinstance(other, Color):
            return super().__eq__(other)
        if isinstance(other, str):
            return self.value == other or self.value == other.lower()
        return False