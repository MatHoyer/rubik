from functools import lru_cache
from typing import NamedTuple


class Color:
    value: str
    print: str
    hex: str

    def __init__(self, value: str, print_code: str, hex_code: str):
        self.value = value
        self.print = print_code
        self.hex = hex_code

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


class Colors(NamedTuple):
    WHITE:  Color = Color("White",  "\033[47m \033[0m",         "#FFFFFF")
    YELLOW: Color = Color("Yellow", "\033[43m \033[0m",         "#FFFF00")
    RED:    Color = Color("Red",    "\033[41m \033[0m",         "#FF0000")
    ORANGE: Color = Color("Orange", "\033[48;5;208m \033[0m",   "#FFAA00")
    BLUE:   Color = Color("Blue",   "\033[44m \033[0m",         "#0000FF")
    GREEN:  Color = Color("Green",  "\033[42m \033[0m",         "#00FF00")
    BLACK:  Color = Color("Black",  "\033[40m \033[0m",         "#000000")


@lru_cache(maxsize=1)
def get_colors():
    return Colors()
