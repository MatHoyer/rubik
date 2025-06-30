import numpy as np
import logging
from typing import List
import random

from .Color import Color, c
from .Position import Position, PRIME, DOUBLE


class Face:
    def __init__(self, color: Color) -> None:
        self._content = np.full((3, 3), color, dtype=str)

    def __str__(self):
        return str(self._content)

    def __getitem__(self, key):
        return self._content[key]

    def __setitem__(self, key, value):
        self._content[key] = value

    def get_center(self):
        return self._content[1][1]

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
    _front = Face(Color.BLUE)
    _back = Face(Color.GREEN)

    _top = Face(Color.YELLOW)
    _bottom = Face(Color.WHITE)

    _right = Face(Color.RED)
    _left = Face(Color.ORANGE)

    def __init__(self, mix: str | int) -> None:
        if isinstance(mix, int):
            logging.info('Start random mix')
            mix = self.random_mix(length=mix)
            logging.info(f'Random mix is: {mix}')
        instructions = mix.strip().split(' ')
        for instruction in instructions:
            assert 1 <= len(instruction) <= 2
            for char in instruction:
                assert char in Position.get_positions() or char in [PRIME, DOUBLE]
        for instruction in instructions:
            self.find_good_action(instruction=instruction)

    def __str__(self):
        return f'''
        ┌───────┐
        │ {' '.join(map(c, self._top[0]))} │
        │ {' '.join(map(c, self._top[1]))} │
        │ {' '.join(map(c, self._top[2]))} │
┌───────┼───────┼───────┬───────┐
│ {' '.join(map(c, self._left[0]))} │ {' '.join(map(c, self._front[0]))} │ \
{' '.join(map(c, self._right[0]))} │ {' '.join(map(c, self._back[0]))} │
│ {' '.join(map(c, self._left[1]))} │ {' '.join(map(c, self._front[1]))} │ \
{' '.join(map(c, self._right[1]))} │ {' '.join(map(c, self._back[1]))} │
│ {' '.join(map(c, self._left[2]))} │ {' '.join(map(c, self._front[2]))} │ \
{' '.join(map(c, self._right[2]))} │ {' '.join(map(c, self._back[2]))} │
└───────┼───────┼───────┴───────┘
        │ {' '.join(map(c, self._bottom[0]))} │
        │ {' '.join(map(c, self._bottom[1]))} │
        │ {' '.join(map(c, self._bottom[2]))} │
        └───────┘
'''

    @staticmethod
    def get_line(face: Face, index: int):
        return np.copy(face[index])

    @staticmethod
    def get_col(face: Face, index: int):
        col = []
        for i in range(3):
            col.append(face[i][index])
        return np.copy(col)

    @staticmethod
    def random_mix(length: int):
        mix = []
        positions = Position.get_positions()
        for _ in range(length):
            instruction = '' + random.choice(positions).value
            instruction += random.choice([PRIME, DOUBLE, ''])
            mix.append(instruction)
        return ' '.join(mix)

    def find_good_action(self, instruction: str) -> None:
        '''
        Instruction is a max 2caracs string like: "U", "F2"
        '''
        position = Position.get_good_position(pos=instruction[0])

        if len(instruction) == 1:
            self.rotate(position=position)
        elif instruction[1] == PRIME:
            self.counter_rotate(position=position)
        elif instruction[1] == DOUBLE:
            self.double_rotate(position=position)

    def rotate(self, position: Position, _from_double_rotate=False) -> None:
        if not _from_double_rotate:
            logging.info(f'rotate: {position}')

        match position:
            case Position.TOP:
                colors_front = self.get_line(face=self._front, index=0)
                colors_right = self.get_line(face=self._right, index=0)
                colors_left = self.get_line(face=self._left, index=0)
                colors_back = self.get_line(face=self._back, index=0)
                self._top.rotate()
                self._front.change_line(index=0, colors=colors_right)
                self._left.change_line(index=0, colors=colors_front)
                self._back.change_line(index=0, colors=colors_left)
                self._right.change_line(index=0, colors=colors_back)
            case Position.BOTTOM:
                colors_front = self.get_line(face=self._front, index=2)
                colors_right = self.get_line(face=self._right, index=2)
                colors_left = self.get_line(face=self._left, index=2)
                colors_back = self.get_line(face=self._back, index=2)
                self._bottom.rotate()
                self._front.change_line(index=2, colors=colors_left)
                self._left.change_line(index=2, colors=colors_back)
                self._back.change_line(index=2, colors=colors_right)
                self._right.change_line(index=2, colors=colors_front)
            case Position.LEFT:
                colors_front = self.get_col(face=self._front, index=0)
                colors_top = self.get_col(face=self._top, index=0)
                colors_bottom = self.get_col(face=self._bottom, index=0)
                colors_back = self.get_col(face=self._back, index=0)
                self._left.rotate()
                self._front.change_col(index=0, colors=colors_top)
                self._top.change_col(index=0, colors=colors_back)
                self._back.change_col(index=0, colors=colors_bottom)
                self._bottom.change_col(index=0, colors=colors_front)
            case Position.RIGHT:
                colors_front = self.get_col(face=self._front, index=2)
                colors_top = self.get_col(face=self._top, index=2)
                colors_bottom = self.get_col(face=self._bottom, index=2)
                colors_back = self.get_col(face=self._back, index=2)
                self._right.rotate()
                self._front.change_col(index=2, colors=colors_bottom)
                self._top.change_col(index=2, colors=colors_front)
                self._back.change_col(index=2, colors=colors_top)
                self._bottom.change_col(index=2, colors=colors_back)
            case Position.FRONT:
                self._front.rotate()
            case Position.BACK:
                self._back.counter_rotate()

    def counter_rotate(self, position: Position) -> None:
        logging.info(f'counter_rotate: {position}')
        match position:
            case Position.TOP:
                colors_front = self.get_line(face=self._front, index=0)
                colors_right = self.get_line(face=self._right, index=0)
                colors_left = self.get_line(face=self._left, index=0)
                colors_back = self.get_line(face=self._back, index=0)
                self._bottom.rotate()
                self._front.change_line(index=0, colors=colors_left)
                self._left.change_line(index=0, colors=colors_back)
                self._back.change_line(index=0, colors=colors_right)
                self._right.change_line(index=0, colors=colors_front)
            case Position.BOTTOM:
                colors_front = self.get_line(face=self._front, index=2)
                colors_right = self.get_line(face=self._right, index=2)
                colors_left = self.get_line(face=self._left, index=2)
                colors_back = self.get_line(face=self._back, index=2)
                self._top.rotate()
                self._front.change_line(index=2, colors=colors_right)
                self._left.change_line(index=2, colors=colors_front)
                self._back.change_line(index=2, colors=colors_left)
                self._right.change_line(index=2, colors=colors_back)
            case Position.LEFT:
                colors_front = self.get_col(face=self._front, index=0)
                colors_top = self.get_col(face=self._top, index=0)
                colors_bottom = self.get_col(face=self._bottom, index=0)
                colors_back = self.get_col(face=self._back, index=0)
                self._right.rotate()
                self._front.change_col(index=0, colors=colors_bottom)
                self._top.change_col(index=0, colors=colors_front)
                self._back.change_col(index=0, colors=colors_top)
                self._bottom.change_col(index=0, colors=colors_back)
            case Position.RIGHT:
                colors_front = self.get_col(face=self._front, index=2)
                colors_top = self.get_col(face=self._top, index=2)
                colors_bottom = self.get_col(face=self._bottom, index=2)
                colors_back = self.get_col(face=self._back, index=2)
                self._left.rotate()
                self._front.change_col(index=2, colors=colors_top)
                self._top.change_col(index=2, colors=colors_back)
                self._back.change_col(index=2, colors=colors_bottom)
                self._bottom.change_col(index=2, colors=colors_front)
            case Position.FRONT:
                self._front.counter_rotate()
            case Position.BACK:
                self._back.rotate()

    def double_rotate(self, position: Position) -> None:
        logging.info(f'double_rotate: {position}')
        for _ in range(2):
            self.rotate(position=position, _from_double_rotate=True)
