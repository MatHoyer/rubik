from enum import Enum

PRIME = '\''
DOUBLE = '2'

class Position(Enum):
    TOP = 'U'
    BOTTOM = 'D'
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

    def __str__(self):
        return self.value

    def __eq__(self, other: object | str) -> bool:
        if isinstance(other, Position):
            return super().__eq__(other)
        if isinstance(other, str):
            return self.value == other or self.value == other.lower()
        return False
