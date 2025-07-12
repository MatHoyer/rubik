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
    WHITE:  Color = Color("White",  "W", "#FFFFFF")
    YELLOW: Color = Color("Yellow", "Y", "#FFFF00")
    RED:    Color = Color("Red",    "R", "#FF0000")
    ORANGE: Color = Color("Orange", "O", "#FFAA00")
    BLUE:   Color = Color("Blue",   "B", "#0000FF")
    GREEN:  Color = Color("Green",  "G", "#00FF00")
    BLACK:  Color = Color("Black",  "K", "#000000")


@lru_cache(maxsize=1)
def get_colors():
    return Colors()
