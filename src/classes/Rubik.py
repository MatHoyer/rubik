import numpy as np
import logging
from typing import List, NamedTuple
import random

from .Color import Color, c
from .Position import Position, PRIME, DOUBLE


class Faces(NamedTuple):
    front: np.typing.NDArray
    back: np.typing.NDArray
    top: np.typing.NDArray
    bottom: np.typing.NDArray
    right: np.typing.NDArray
    left: np.typing.NDArray


class Face:
    def __init__(self, color: Color) -> None:
        self._content = np.full((3, 3), color, dtype=str)

    def __str__(self):
        return str(self._content)

    def __getitem__(self, key):
        return self._content[key]

    def __setitem__(self, key, value):
        self._content[key] = value

    def get_face_color(self):
        return self._content[1][1]

    # Resolve
    def is_cross(self):
        face_color = self.get_face_color()
        top_mid = self._content[0][1]
        mid_left = self._content[1][0]
        mid_right = self._content[1][2]
        bottom_mid = self._content[2][1]
        return top_mid == mid_left == mid_right == bottom_mid == face_color

    def find_color_col(self, index: int, color: Color):
        col = []
        for i in range(3):
            col.append(self._content[i][index])
        return color in col

    def find_color_line(self, index: int, color: Color):
        return color in self._content[index]

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
            raise ValueError(f'Invalid index: expected between 0 and 2 get {index}')

        self._content[index] = colors

    def change_col(self, index: int, colors: List[Color]):
        if not 0 <= index <= 2:
            raise ValueError(f'Invalid index: expected between 0 and 2 get {index}')

        for i in range(3):
            self._content[i][index] = colors[i]

    def rotate(self):
        self._content = np.rot90(self._content, k=3)

    def counter_rotate(self):
        self._content = np.rot90(self._content)


class Rubik:
    front = Face(Color.GREEN)
    back = Face(Color.BLUE)

    top = Face(Color.WHITE)
    bottom = Face(Color.YELLOW)

    right = Face(Color.RED)
    left = Face(Color.ORANGE)

    mix: List[str] = []
    solution: List[str] = []

    def __init__(self, mix: str | int) -> None:
        if isinstance(mix, int):
            logging.info('Start random mix')
            mix = self.random_mix(length=mix)
            logging.info(f'Random mix is: {mix}')
        self.mix = mix.strip().split(' ')
        for instruction in self.mix:
            assert 1 <= len(instruction) <= 2
            assert instruction[0] in Position.get_positions()
            if len(instruction) == 2:
                assert instruction[1] in [*PRIME, DOUBLE]
        for instruction in self.mix:
            self.find_good_action(instruction=instruction)

    def __str__(self):
        return f'''
        ┌───────┐
        │ {' '.join(map(c, self.top[0]))} │
        │ {' '.join(map(c, self.top[1]))} │
        │ {' '.join(map(c, self.top[2]))} │
┌───────┼───────┼───────┬───────┐
│ {' '.join(map(c, self.left[0]))} │ {' '.join(map(c, self.front[0]))} │ \
{' '.join(map(c, self.right[0]))} │ {' '.join(map(c, self.back[0][::-1]))} │
│ {' '.join(map(c, self.left[1]))} │ {' '.join(map(c, self.front[1]))} │ \
{' '.join(map(c, self.right[1]))} │ {' '.join(map(c, self.back[1][::-1]))} │
│ {' '.join(map(c, self.left[2]))} │ {' '.join(map(c, self.front[2]))} │ \
{' '.join(map(c, self.right[2]))} │ {' '.join(map(c, self.back[2][::-1]))} │
└───────┼───────┼───────┴───────┘
        │ {' '.join(map(c, self.bottom[0]))} │
        │ {' '.join(map(c, self.bottom[1]))} │
        │ {' '.join(map(c, self.bottom[2]))} │
        └───────┘
'''

    @staticmethod
    def random_mix(length: int):
        mix = []
        positions = Position.get_positions()
        for _ in range(length):
            instruction = '' + random.choice(positions).value
            instruction += random.choice([PRIME[0], DOUBLE, ''])
            mix.append(instruction)
        return ' '.join(mix)

    def get_faces(self):
        return Faces(
            front=self.front._content,
            back=self.back._content,
            top=self.top._content,
            bottom=self.bottom._content,
            right=self.right._content,
            left=self.left._content,
        )

    # Resolve
    def step_cross(self):
        if self.front.is_cross():
            return
        front_color = self.front.get_face_color()
        if self.front[0][1] != front_color:
            pass
        if self.front[1][0] != front_color:
            pass
        if self.front[1][2] != front_color:
            pass
        if self.front[2][1] != front_color:
            pass

    def resolve(self):
        self.step_cross()

    # Moves
    def find_good_action(self, instruction: str, _for_solution=False) -> None:
        '''
        Instruction is a max 2caracs string like: "U", "F2"
        '''
        position = Position.get_good_position(pos=instruction[0])

        if len(instruction) == 1:
            self.rotate(position=position)
        elif instruction[1] in PRIME:
            self.counter_rotate(position=position)
        elif instruction[1] == DOUBLE:
            self.double_rotate(position=position)
        if _for_solution:
            self.solution.append(position)

    def rotate(self, position: Position, _from_double_rotate=False) -> None:
        if not _from_double_rotate:
            logging.info(f'rotate: {position}')

        match position:
            case Position.TOP:
                colors_front = self.front.get_line(index=0)
                colors_right = self.right.get_line(index=0)
                colors_left = self.left.get_line(index=0)
                colors_back = self.back.get_line(index=0)
                self.top.rotate()
                self.front.change_line(index=0, colors=colors_right)
                self.left.change_line(index=0, colors=colors_front)
                self.back.change_line(index=0, colors=colors_left[::-1])
                self.right.change_line(index=0, colors=colors_back[::-1])
            case Position.BOTTOM:
                colors_front = self.front.get_line(index=2)
                colors_right = self.right.get_line(index=2)
                colors_left = self.left.get_line(index=2)
                colors_back = self.back.get_line(index=2)
                self.bottom.rotate()
                self.front.change_line(index=2, colors=colors_left)
                self.left.change_line(index=2, colors=colors_back[::-1])
                self.back.change_line(index=2, colors=colors_right[::-1])
                self.right.change_line(index=2, colors=colors_front)
            case Position.LEFT:
                colors_front = self.front.get_col(index=0)
                colors_top = self.top.get_col(index=0)
                colors_bottom = self.bottom.get_col(index=0)
                colors_back = self.back.get_col(index=0)
                self.left.rotate()
                self.front.change_col(index=0, colors=colors_top)
                self.top.change_col(index=0, colors=colors_back[::-1])
                self.back.change_col(index=0, colors=colors_bottom[::-1])
                self.bottom.change_col(index=0, colors=colors_front)
            case Position.RIGHT:
                colors_front = self.front.get_col(index=2)
                colors_top = self.top.get_col(index=2)
                colors_bottom = self.bottom.get_col(index=2)
                colors_back = self.back.get_col(index=2)
                self.right.rotate()
                self.front.change_col(index=2, colors=colors_bottom)
                self.top.change_col(index=2, colors=colors_front)
                self.back.change_col(index=2, colors=colors_top[::-1])
                self.bottom.change_col(index=2, colors=colors_back[::-1])
            case Position.FRONT:
                colors_top = self.top.get_line(index=2)
                colors_right = self.right.get_col(index=0)
                colors_bottom = self.bottom.get_line(index=0)
                colors_left = self.left.get_col(index=2)
                self.front.rotate()
                self.top.change_line(index=2, colors=colors_left[::-1])
                self.right.change_col(index=0, colors=colors_top)
                self.bottom.change_line(index=0, colors=colors_right[::-1])
                self.left.change_col(index=2, colors=colors_bottom)
            case Position.BACK:
                colors_top = self.top.get_line(index=0)
                colors_right = self.right.get_col(index=2)
                colors_bottom = self.bottom.get_line(index=2)
                colors_left = self.left.get_col(index=0)
                self.back.counter_rotate()
                self.top.change_line(index=0, colors=colors_right)
                self.right.change_col(index=2, colors=colors_bottom[::-1])
                self.bottom.change_line(index=2, colors=colors_left)
                self.left.change_col(index=0, colors=colors_top[::-1])

    def counter_rotate(self, position: Position) -> None:
        logging.info(f'counter_rotate: {position}')
        match position:
            case Position.TOP:
                colors_front = self.front.get_line(index=0)
                colors_right = self.right.get_line(index=0)
                colors_left = self.left.get_line(index=0)
                colors_back = self.back.get_line(index=0)
                self.top.counter_rotate()
                self.front.change_line(index=0, colors=colors_left)
                self.left.change_line(index=0, colors=colors_back[::-1])
                self.back.change_line(index=0, colors=colors_right[::-1])
                self.right.change_line(index=0, colors=colors_front)
            case Position.BOTTOM:
                colors_front = self.front.get_line(index=2)
                colors_right = self.right.get_line(index=2)
                colors_left = self.left.get_line(index=2)
                colors_back = self.back.get_line(index=2)
                self.bottom.counter_rotate()
                self.front.change_line(index=2, colors=colors_right)
                self.left.change_line(index=2, colors=colors_front)
                self.back.change_line(index=2, colors=colors_left[::-1])
                self.right.change_line(index=2, colors=colors_back[::-1])
            case Position.LEFT:
                colors_front = self.front.get_col(index=0)
                colors_top = self.top.get_col(index=0)
                colors_bottom = self.bottom.get_col(index=0)
                colors_back = self.back.get_col(index=0)
                self.left.counter_rotate()
                self.front.change_col(index=0, colors=colors_bottom)
                self.top.change_col(index=0, colors=colors_front)
                self.back.change_col(index=0, colors=colors_top[::-1])
                self.bottom.change_col(index=0, colors=colors_back[::-1])
            case Position.RIGHT:
                colors_front = self.front.get_col(index=2)
                colors_top = self.top.get_col(index=2)
                colors_bottom = self.bottom.get_col(index=2)
                colors_back = self.back.get_col(index=2)
                self.right.counter_rotate()
                self.front.change_col(index=2, colors=colors_top)
                self.top.change_col(index=2, colors=colors_back[::-1])
                self.back.change_col(index=2, colors=colors_bottom[::-1])
                self.bottom.change_col(index=2, colors=colors_front)
            case Position.FRONT:
                colors_top = self.top.get_line(index=2)
                colors_right = self.right.get_col(index=0)
                colors_bottom = self.bottom.get_line(index=0)
                colors_left = self.left.get_col(index=2)
                self.front.counter_rotate()
                self.top.change_line(index=2, colors=colors_right)
                self.right.change_col(index=0, colors=colors_bottom[::-1])
                self.bottom.change_line(index=0, colors=colors_left)
                self.left.change_col(index=2, colors=colors_top[::-1])
            case Position.BACK:
                colors_top = self.top.get_line(index=0)
                colors_right = self.right.get_col(index=2)
                colors_bottom = self.bottom.get_line(index=2)
                colors_left = self.left.get_col(index=0)
                self.back.rotate()
                self.top.change_line(index=0, colors=colors_left[::-1])
                self.right.change_col(index=2, colors=colors_top)
                self.bottom.change_line(index=2, colors=colors_right[::-1])
                self.left.change_col(index=0, colors=colors_bottom)

    def double_rotate(self, position: Position) -> None:
        logging.info(f'double_rotate: {position}')
        for _ in range(2):
            self.rotate(position=position, _from_double_rotate=True)
