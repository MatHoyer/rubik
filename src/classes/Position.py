from enum import Enum

PRIME = ['\'', '’']
DOUBLE = '2'


class Position(Enum):
    UP = 'U'
    DOWN = 'D'
    RIGHT = 'R'
    LEFT = 'L'
    FRONT = 'F'
    BACK = 'B'

    @staticmethod
    def get_positions():
        return list(Position)

    @staticmethod
    def get_good_position(pos: str):
        positions = Position.get_positions()
        position_index = positions.index(pos)
        return positions[position_index]

    def clockwise(self):
        return self.value

    def counter_clockwise(self):
        return self.value + PRIME[0]

    def double_clockwise(self):
        return self.value + DOUBLE

    def __str__(self):
        return self.value

    def __eq__(self, other: object | str) -> bool:
        if isinstance(other, Position):
            return super().__eq__(other)
        if isinstance(other, str):
            return self.value == other or self.value == other.lower()
        return False
