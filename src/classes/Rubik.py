import numpy as np
import logging
from typing import List, NamedTuple
import random
from functools import lru_cache

from .Color import Color, get_colors_faces
from .Position import Position, PRIME, DOUBLE


class Faces(NamedTuple):
    front:  List[List[Color]]
    back:   List[List[Color]]
    up:     List[List[Color]]
    down:   List[List[Color]]
    right:  List[List[Color]]
    left:   List[List[Color]]


class Face:
    def __init__(self, color: Color) -> None:
        self._content = np.full((3, 3), fill_value=color, dtype=object)

    def __str__(self):
        return str(self._content)

    def __getitem__(self, key) -> List[Color]:
        return self._content[key]

    def get_color(self) -> Color:
        return self._content[1, 1]

    # Moves
    def get_line(self, index: int):
        return np.copy(self._content[index])

    def get_col(self, index: int):
        col = []
        for i in range(3):
            col.append(self._content[i][index])
        return np.copy(col)

    def change_line(self, index: int, colors: List[Color]):
        if not 0 <= index <= 2:
            raise ValueError(f"Invalid index: expected between 0 and 2 get {index}")

        self._content[index] = colors

    def change_col(self, index: int, colors: List[Color]):
        if not 0 <= index <= 2:
            raise ValueError(f"Invalid index: expected between 0 and 2 get {index}")

        for i in range(3):
            self._content[i][index] = colors[i]

    def clockwise_rotate(self):
        self._content = np.rot90(self._content, k=3)

    def counter_clockwise_rotate(self):
        self._content = np.rot90(self._content)


class Rubik:
    up = Face(get_colors_faces().FRONT.up)
    down = Face(get_colors_faces().FRONT.down)
    front = Face(get_colors_faces().FRONT.front)
    back = Face(get_colors_faces().FRONT.back)
    left = Face(get_colors_faces().FRONT.left)
    right = Face(get_colors_faces().FRONT.right)

    mix = np.array([])
    solution = np.array([])

    def __init__(self, mix: str | int) -> None:
        if isinstance(mix, int):
            logging.info("Start random mix")
            mix = self.random_mix(length=mix)
            logging.info(f"Random mix is: {mix}")
        self.mix = np.array(mix.strip().split(" "))
        for instruction in self.mix:
            assert 1 <= len(instruction) <= 2
            assert instruction[0] in Position.get_positions()
            if len(instruction) == 2:
                assert instruction[1] in [*PRIME, DOUBLE]
        for instruction in self.mix:
            self.find_good_action(instruction=instruction)

    def __str__(self):
        return f"""
        ┌───────┐
        │ {" ".join([color.print for color in self.up[0]])} │
        │ {" ".join([color.print for color in self.up[1]])} │
        │ {" ".join([color.print for color in self.up[2]])} │
┌───────┼───────┼───────┬───────┐
│ {" ".join([color.print for color in self.left[0]])} │ {" ".join([color.print for color in self.front[0]])} │ \
{" ".join([color.print for color in self.right[0]])} │ {" ".join([color.print for color in self.back[0][::-1]])} │
│ {" ".join([color.print for color in self.left[1]])} │ {" ".join([color.print for color in self.front[1]])} │ \
{" ".join([color.print for color in self.right[1]])} │ {" ".join([color.print for color in self.back[1][::-1]])} │
│ {" ".join([color.print for color in self.left[2]])} │ {" ".join([color.print for color in self.front[2]])} │ \
{" ".join([color.print for color in self.right[2]])} │ {" ".join([color.print for color in self.back[2][::-1]])} │
└───────┼───────┼───────┴───────┘
        │ {" ".join([color.print for color in self.down[0]])} │
        │ {" ".join([color.print for color in self.down[1]])} │
        │ {" ".join([color.print for color in self.down[2]])} │
        └───────┘
"""

    @staticmethod
    def random_mix(length: int):
        mix = []
        positions = Position.get_positions()
        for _ in range(length):
            instruction = "" + random.choice(positions).value
            instruction += random.choice([PRIME[0], DOUBLE, ""])
            mix.append(instruction)
        return " ".join(mix)

    @lru_cache(maxsize=1)
    def get_faces(self):
        return Faces(
            front=self.front._content,
            back=self.back._content,
            up=self.up._content,
            down=self.down._content,
            right=self.right._content,
            left=self.left._content,
        )

    # Moves
    def find_good_action(self, instruction: str, _for_solution=False) -> None:
        """
        Instruction is a max 2caracs string like: "U", "F2"
        """
        position = Position.get_good_position(pos=instruction[0])

        if len(instruction) == 1:
            self.clockwise_rotate(position=position)
        elif instruction[1] in PRIME:
            self.counter_clockwise_rotate(position=position)
        elif instruction[1] == DOUBLE:
            self.double_clockwise_rotate(position=position)
        if _for_solution:
            self.solution.append(position)

    def clockwise_rotate(self, position: Position, _from_double_rotate=False) -> None:
        if not _from_double_rotate:
            logging.info(f"rotate: {position}")

        match position:
            case Position.UP:
                colors_front = self.front.get_line(index=0)
                colors_right = self.right.get_line(index=0)
                colors_left = self.left.get_line(index=0)
                colors_back = self.back.get_line(index=0)
                self.up.clockwise_rotate()
                self.front.change_line(index=0, colors=colors_right)
                self.left.change_line(index=0, colors=colors_front)
                self.back.change_line(index=0, colors=colors_left[::-1])
                self.right.change_line(index=0, colors=colors_back[::-1])
            case Position.DOWN:
                colors_front = self.front.get_line(index=2)
                colors_right = self.right.get_line(index=2)
                colors_left = self.left.get_line(index=2)
                colors_back = self.back.get_line(index=2)
                self.down.clockwise_rotate()
                self.front.change_line(index=2, colors=colors_left)
                self.left.change_line(index=2, colors=colors_back[::-1])
                self.back.change_line(index=2, colors=colors_right[::-1])
                self.right.change_line(index=2, colors=colors_front)
            case Position.LEFT:
                colors_front = self.front.get_col(index=0)
                colors_up = self.up.get_col(index=0)
                colors_down = self.down.get_col(index=0)
                colors_back = self.back.get_col(index=0)
                self.left.clockwise_rotate()
                self.front.change_col(index=0, colors=colors_up)
                self.up.change_col(index=0, colors=colors_back[::-1])
                self.back.change_col(index=0, colors=colors_down[::-1])
                self.down.change_col(index=0, colors=colors_front)
            case Position.RIGHT:
                colors_front = self.front.get_col(index=2)
                colors_up = self.up.get_col(index=2)
                colors_down = self.down.get_col(index=2)
                colors_back = self.back.get_col(index=2)
                self.right.clockwise_rotate()
                self.front.change_col(index=2, colors=colors_down)
                self.up.change_col(index=2, colors=colors_front)
                self.back.change_col(index=2, colors=colors_up[::-1])
                self.down.change_col(index=2, colors=colors_back[::-1])
            case Position.FRONT:
                colors_up = self.up.get_line(index=2)
                colors_right = self.right.get_col(index=0)
                colors_down = self.down.get_line(index=0)
                colors_left = self.left.get_col(index=2)
                self.front.clockwise_rotate()
                self.up.change_line(index=2, colors=colors_left[::-1])
                self.right.change_col(index=0, colors=colors_up)
                self.down.change_line(index=0, colors=colors_right[::-1])
                self.left.change_col(index=2, colors=colors_down)
            case Position.BACK:
                colors_up = self.up.get_line(index=0)
                colors_right = self.right.get_col(index=2)
                colors_down = self.down.get_line(index=2)
                colors_left = self.left.get_col(index=0)
                self.back.counter_clockwise_rotate()
                self.up.change_line(index=0, colors=colors_right)
                self.right.change_col(index=2, colors=colors_down[::-1])
                self.down.change_line(index=2, colors=colors_left)
                self.left.change_col(index=0, colors=colors_up[::-1])

    def counter_clockwise_rotate(self, position: Position) -> None:
        logging.info(f"counter_rotate: {position}")
        match position:
            case Position.UP:
                colors_front = self.front.get_line(index=0)
                colors_right = self.right.get_line(index=0)
                colors_left = self.left.get_line(index=0)
                colors_back = self.back.get_line(index=0)
                self.up.counter_clockwise_rotate()
                self.front.change_line(index=0, colors=colors_left)
                self.left.change_line(index=0, colors=colors_back[::-1])
                self.back.change_line(index=0, colors=colors_right[::-1])
                self.right.change_line(index=0, colors=colors_front)
            case Position.DOWN:
                colors_front = self.front.get_line(index=2)
                colors_right = self.right.get_line(index=2)
                colors_left = self.left.get_line(index=2)
                colors_back = self.back.get_line(index=2)
                self.down.counter_clockwise_rotate()
                self.front.change_line(index=2, colors=colors_right)
                self.left.change_line(index=2, colors=colors_front)
                self.back.change_line(index=2, colors=colors_left[::-1])
                self.right.change_line(index=2, colors=colors_back[::-1])
            case Position.LEFT:
                colors_front = self.front.get_col(index=0)
                colors_up = self.up.get_col(index=0)
                colors_down = self.down.get_col(index=0)
                colors_back = self.back.get_col(index=0)
                self.left.counter_clockwise_rotate()
                self.front.change_col(index=0, colors=colors_down)
                self.up.change_col(index=0, colors=colors_front)
                self.back.change_col(index=0, colors=colors_up[::-1])
                self.down.change_col(index=0, colors=colors_back[::-1])
            case Position.RIGHT:
                colors_front = self.front.get_col(index=2)
                colors_up = self.up.get_col(index=2)
                colors_down = self.down.get_col(index=2)
                colors_back = self.back.get_col(index=2)
                self.right.counter_clockwise_rotate()
                self.front.change_col(index=2, colors=colors_up)
                self.up.change_col(index=2, colors=colors_back[::-1])
                self.back.change_col(index=2, colors=colors_down[::-1])
                self.down.change_col(index=2, colors=colors_front)
            case Position.FRONT:
                colors_up = self.up.get_line(index=2)
                colors_right = self.right.get_col(index=0)
                colors_down = self.down.get_line(index=0)
                colors_left = self.left.get_col(index=2)
                self.front.counter_clockwise_rotate()
                self.up.change_line(index=2, colors=colors_right)
                self.right.change_col(index=0, colors=colors_down[::-1])
                self.down.change_line(index=0, colors=colors_left)
                self.left.change_col(index=2, colors=colors_up[::-1])
            case Position.BACK:
                colors_up = self.up.get_line(index=0)
                colors_right = self.right.get_col(index=2)
                colors_down = self.down.get_line(index=2)
                colors_left = self.left.get_col(index=0)
                self.back.clockwise_rotate()
                self.up.change_line(index=0, colors=colors_left[::-1])
                self.right.change_col(index=2, colors=colors_up)
                self.down.change_line(index=2, colors=colors_right[::-1])
                self.left.change_col(index=0, colors=colors_down)

    def double_clockwise_rotate(self, position: Position) -> None:
        logging.info(f"double_rotate: {position}")
        for _ in range(2):
            self.clockwise_rotate(position=position, _from_double_rotate=True)
