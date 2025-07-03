from enum import Enum


class Color(Enum):
    WHITE = 'W'
    YELLOW = 'Y'
    RED = 'R'
    ORANGE = 'O'
    BLUE = 'B'
    GREEN = 'G'
    BLACK = 'black'

    def __str__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: object | str) -> bool:
        if isinstance(other, Color):
            return super().__eq__(other)
        if isinstance(other, str):
            return self.value == other or self.value == other.lower()
        return False


def c(color: Color):
    match color:
        case Color.BLUE:
            return "\033[44m \033[0m"
        case Color.GREEN:
            return "\033[42m \033[0m"
        case Color.YELLOW:
            return "\033[43m \033[0m"
        case Color.WHITE:
            return "\033[47m \033[0m"
        case Color.RED:
            return "\033[41m \033[0m"
        case Color.ORANGE:
            return "\033[48;5;208m \033[0m"
        case _:
            raise ValueError('Invalid color')


colors = {
    Color.WHITE: '#FFFFFF',
    Color.YELLOW: '#FFFF00',
    Color.RED: '#FF0000',
    Color.ORANGE: "#FFAA00",
    Color.BLUE: '#0000FF',
    Color.GREEN: '#00FF00',
    Color.BLACK: "#000000"
}
