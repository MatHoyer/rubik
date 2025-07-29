from .Position import Position
from typing import Callable, List


class Edges:
    UP_BACK = 0
    UP_LEFT = 1
    UP_RIGHT = 2
    UP_FRONT = 3
    DOWN_FRONT = 4
    DOWN_LEFT = 5
    DOWN_RIGHT = 6
    DOWN_BACK = 7
    FRONT_LEFT = 8
    FRONT_RIGHT = 9
    BACK_LEFT = 10
    BACK_RIGHT = 11


def case_2_bad_edges(bad_edges: List[int], front_nb: int, back_nb: int, do_moves: Callable):
    if front_nb:
        if front_nb == 2:
            if bad_edges[Edges.UP_FRONT]:
                do_moves([Position.UP.clockwise()])
            elif bad_edges[Edges.FRONT_LEFT]:
                do_moves([Position.LEFT.clockwise()])
            else:
                do_moves([Position.RIGHT.clockwise()])
        do_moves([Position.FRONT.clockwise()])
    else:
        if back_nb:
            if back_nb == 2:
                if bad_edges[Edges.UP_BACK]:
                    do_moves([Position.UP.clockwise()])
                elif bad_edges[Edges.BACK_LEFT]:
                    do_moves([Position.LEFT.clockwise()])
                else:
                    do_moves([Position.RIGHT.clockwise()])
            do_moves([Position.BACK.clockwise()])
        else:
            if bad_edges[2]:
                do_moves([Position.RIGHT.counter_clockwise()])
            elif bad_edges[6]:
                do_moves([Position.RIGHT.clockwise()])
            elif bad_edges[1]:
                do_moves([Position.LEFT.clockwise()])
            elif bad_edges[5]:
                do_moves([Position.LEFT.counter_clockwise()])
            do_moves([Position.FRONT.clockwise()])


def case_6_bad_edges(bad_edges: List[int], front_nb: int, back_nb: int, do_moves: Callable):
    if front_nb >= back_nb:
        if front_nb == 1:
            if bad_edges[Edges.UP_FRONT] or bad_edges[Edges.DOWN_FRONT]:
                do_moves([Position.LEFT.clockwise(), Position.RIGHT.clockwise()])
            else:
                do_moves([Position.UP.clockwise(), Position.DOWN.clockwise()])
        elif front_nb == 2:
            done = False
            if not bad_edges[Edges.UP_FRONT]:
                done = True
                if bad_edges[Edges.UP_LEFT]:
                    do_moves([Position.UP.counter_clockwise()])
                elif bad_edges[Edges.UP_RIGHT]:
                    do_moves([Position.UP.clockwise()])
                elif bad_edges[Edges.UP_BACK]:
                    do_moves([Position.UP.double_clockwise()])
                else:
                    done = False
            if not done and not bad_edges[Edges.DOWN_FRONT]:
                done = True
                if bad_edges[Edges.DOWN_LEFT]:
                    do_moves([Position.DOWN.clockwise()])
                elif bad_edges[Edges.DOWN_RIGHT]:
                    do_moves([Position.DOWN.counter_clockwise()])
                elif bad_edges[Edges.DOWN_BACK]:
                    do_moves([Position.DOWN.double_clockwise()])
                else:
                    done = False
            if not done and not bad_edges[Edges.FRONT_LEFT]:
                done = True
                if bad_edges[Edges.UP_LEFT]:
                    do_moves([Position.LEFT.clockwise()])
                elif bad_edges[Edges.DOWN_LEFT]:
                    do_moves([Position.LEFT.counter_clockwise()])
                elif bad_edges[Edges.BACK_LEFT]:
                    do_moves([Position.LEFT.double_clockwise()])
                else:
                    done = False
            if not done and not bad_edges[Edges.FRONT_RIGHT]:
                if bad_edges[Edges.UP_RIGHT]:
                    do_moves([Position.RIGHT.counter_clockwise()])
                elif bad_edges[Edges.DOWN_RIGHT]:
                    do_moves([Position.RIGHT.clockwise()])
                elif bad_edges[Edges.BACK_RIGHT]:
                    do_moves([Position.RIGHT.double_clockwise()])
        elif front_nb == 4:
            if not bad_edges[Edges.UP_LEFT]:
                do_moves([Position.LEFT.clockwise()])
            elif not bad_edges[Edges.DOWN_LEFT]:
                do_moves([Position.LEFT.counter_clockwise()])
            else:
                do_moves([Position.LEFT.double_clockwise()])
        do_moves([Position.FRONT.clockwise()])
    else:
        if back_nb == 1:
            if bad_edges[Edges.UP_BACK] or bad_edges[Edges.DOWN_BACK]:
                do_moves([Position.LEFT.clockwise(), Position.RIGHT.clockwise()])
            else:
                do_moves([Position.UP.clockwise(), Position.DOWN.clockwise()])
        elif back_nb == 2:
            done = False
            if not bad_edges[Edges.UP_BACK]:
                done = True
                if bad_edges[Edges.UP_LEFT]:
                    do_moves([Position.UP.clockwise()])
                elif bad_edges[Edges.UP_RIGHT]:
                    do_moves([Position.UP.counter_clockwise()])
                elif bad_edges[Edges.UP_FRONT]:
                    do_moves([Position.UP.double_clockwise()])
                else:
                    done = False
            if not done and not bad_edges[Edges.DOWN_BACK]:
                done = True
                if bad_edges[Edges.DOWN_LEFT]:
                    do_moves([Position.DOWN.counter_clockwise()])
                elif bad_edges[Edges.DOWN_RIGHT]:
                    do_moves([Position.DOWN.clockwise()])
                elif bad_edges[Edges.DOWN_FRONT]:
                    do_moves([Position.DOWN.double_clockwise()])
                else:
                    done = False
            if not done and not bad_edges[Edges.BACK_RIGHT]:
                done = True
                if bad_edges[Edges.UP_RIGHT]:
                    do_moves([Position.RIGHT.clockwise()])
                elif bad_edges[Edges.DOWN_RIGHT]:
                    do_moves([Position.RIGHT.counter_clockwise()])
                elif bad_edges[Edges.FRONT_RIGHT]:
                    do_moves([Position.RIGHT.double_clockwise()])
                else:
                    done = False
            if not done and not bad_edges[Edges.BACK_LEFT]:
                if bad_edges[Edges.UP_LEFT]:
                    do_moves([Position.LEFT.counter_clockwise()])
                elif bad_edges[Edges.DOWN_LEFT]:
                    do_moves([Position.LEFT.clockwise()])
                elif bad_edges[Edges.FRONT_LEFT]:
                    do_moves([Position.LEFT.double_clockwise()])
        elif back_nb == 4:
            if not bad_edges[Edges.UP_LEFT]:
                do_moves([Position.LEFT.counter_clockwise()])
            elif not bad_edges[Edges.DOWN_LEFT]:
                do_moves([Position.LEFT.clockwise()])
            else:
                do_moves([Position.LEFT.double_clockwise()])
        do_moves([Position.BACK.clockwise()])


def case_default_bad_edges(bad_edges: List[int], front_nb: int, back_nb: int, do_moves: Callable, eo_detection):
    if not front_nb and not back_nb:
        do_moves([
            Position.DOWN.counter_clockwise(),
            Position.LEFT.clockwise(),
            Position.RIGHT.counter_clockwise(),
            Position.FRONT.double_clockwise(),
            Position.DOWN.double_clockwise(),
        ])
        return
    if front_nb >= back_nb:
        if not bad_edges[Edges.UP_FRONT]:
            if bad_edges[Edges.UP_LEFT]:
                do_moves([Position.UP.counter_clockwise()])
            elif bad_edges[Edges.UP_RIGHT]:
                do_moves([Position.UP.clockwise()])
            elif bad_edges[Edges.UP_BACK]:
                do_moves([Position.UP.double_clockwise()])
            elif bad_edges[Edges.DOWN_BACK]:
                do_moves([Position.BACK.double_clockwise(), Position.UP.double_clockwise()])
            elif bad_edges[Edges.BACK_RIGHT]:
                do_moves([
                    Position.RIGHT.counter_clockwise(),
                    Position.UP.clockwise(),
                    Position.RIGHT.clockwise(),
                ])
            elif bad_edges[Edges.DOWN_RIGHT]:
                do_moves([
                    Position.RIGHT.double_clockwise(),
                    Position.UP.clockwise(),
                    Position.RIGHT.double_clockwise(),
                ])
            elif bad_edges[Edges.BACK_LEFT]:
                do_moves([
                    Position.LEFT.clockwise(),
                    Position.UP.counter_clockwise(),
                    Position.LEFT.counter_clockwise(),
                ])
            elif bad_edges[Edges.DOWN_LEFT]:
                do_moves([
                    Position.LEFT.double_clockwise(),
                    Position.UP.counter_clockwise(),
                    Position.LEFT.double_clockwise(),
                ])
            bad_edges = eo_detection()
        if not bad_edges[Edges.DOWN_FRONT]:
            if bad_edges[Edges.DOWN_LEFT]:
                do_moves([Position.DOWN.clockwise()])
            elif bad_edges[Edges.DOWN_RIGHT]:
                do_moves([Position.DOWN.counter_clockwise()])
            elif bad_edges[Edges.DOWN_BACK]:
                do_moves([Position.DOWN.double_clockwise()])
            elif bad_edges[Edges.UP_BACK]:
                do_moves([Position.BACK.double_clockwise(), Position.DOWN.double_clockwise()])
            elif bad_edges[Edges.BACK_RIGHT]:
                do_moves([
                    Position.RIGHT.clockwise(),
                    Position.DOWN.counter_clockwise(),
                    Position.RIGHT.counter_clockwise(),
                ])
            elif bad_edges[Edges.UP_RIGHT]:
                do_moves([
                    Position.RIGHT.double_clockwise(),
                    Position.DOWN.counter_clockwise(),
                    Position.RIGHT.double_clockwise(),
                ])
            elif bad_edges[Edges.BACK_LEFT]:
                do_moves([
                    Position.LEFT.counter_clockwise(),
                    Position.DOWN.clockwise(),
                    Position.LEFT.clockwise(),
                ])
            elif bad_edges[Edges.UP_LEFT]:
                do_moves([
                    Position.LEFT.double_clockwise(),
                    Position.DOWN.clockwise(),
                    Position.LEFT.double_clockwise(),
                ])
            bad_edges = eo_detection()
        if not bad_edges[Edges.FRONT_LEFT]:
            if bad_edges[Edges.UP_LEFT]:
                do_moves([Position.LEFT.clockwise()])
            elif bad_edges[Edges.DOWN_LEFT]:
                do_moves([Position.LEFT.counter_clockwise()])
            elif bad_edges[Edges.BACK_LEFT]:
                do_moves([Position.LEFT.double_clockwise()])
            elif bad_edges[Edges.BACK_RIGHT]:
                do_moves([Position.BACK.double_clockwise(), Position.LEFT.double_clockwise()])
            elif bad_edges[Edges.UP_BACK]:
                do_moves([
                    Position.UP.counter_clockwise(),
                    Position.LEFT.clockwise(),
                    Position.UP.clockwise(),
                ])
            elif bad_edges[Edges.UP_RIGHT]:
                do_moves([
                    Position.UP.double_clockwise(),
                    Position.LEFT.clockwise(),
                    Position.UP.double_clockwise(),
                ])
            elif bad_edges[Edges.DOWN_BACK]:
                do_moves([
                    Position.DOWN.clockwise(),
                    Position.LEFT.counter_clockwise(),
                    Position.DOWN.counter_clockwise(),
                ])
            elif bad_edges[Edges.DOWN_RIGHT]:
                do_moves([
                    Position.DOWN.double_clockwise(),
                    Position.LEFT.counter_clockwise(),
                    Position.DOWN.double_clockwise(),
                ])
            bad_edges = eo_detection()
        if not bad_edges[Edges.FRONT_RIGHT]:
            if bad_edges[Edges.UP_RIGHT]:
                do_moves([Position.RIGHT.counter_clockwise()])
            elif bad_edges[Edges.DOWN_RIGHT]:
                do_moves([Position.RIGHT.clockwise()])
            elif bad_edges[Edges.BACK_RIGHT]:
                do_moves([Position.RIGHT.double_clockwise()])
            elif bad_edges[Edges.BACK_LEFT]:
                do_moves([Position.BACK.double_clockwise(), Position.RIGHT.double_clockwise()])
            elif bad_edges[Edges.UP_BACK]:
                do_moves([
                    Position.UP.clockwise(),
                    Position.RIGHT.counter_clockwise(),
                    Position.UP.counter_clockwise(),
                ])
            elif bad_edges[Edges.UP_LEFT]:
                do_moves([
                    Position.UP.double_clockwise(),
                    Position.RIGHT.counter_clockwise(),
                    Position.UP.double_clockwise(),
                ])
            elif bad_edges[Edges.DOWN_BACK]:
                do_moves([
                    Position.DOWN.counter_clockwise(),
                    Position.RIGHT.clockwise(),
                    Position.DOWN.clockwise(),
                ])
            elif bad_edges[Edges.DOWN_LEFT]:
                do_moves([
                    Position.DOWN.double_clockwise(),
                    Position.RIGHT.clockwise(),
                    Position.DOWN.double_clockwise(),
                ])
        do_moves([Position.FRONT.clockwise()])
    else:
        if not bad_edges[Edges.UP_BACK]:
            if bad_edges[Edges.UP_RIGHT]:
                do_moves([Position.UP.counter_clockwise()])
            elif bad_edges[Edges.UP_LEFT]:
                do_moves([Position.UP.clockwise()])
            elif bad_edges[Edges.UP_FRONT]:
                do_moves([Position.UP.double_clockwise()])
            elif bad_edges[Edges.DOWN_FRONT]:
                do_moves([Position.FRONT.double_clockwise(), Position.UP.double_clockwise()])
            elif bad_edges[Edges.FRONT_RIGHT]:
                do_moves([
                    Position.RIGHT.clockwise(),
                    Position.UP.counter_clockwise(),
                    Position.RIGHT.counter_clockwise(),
                ])
            elif bad_edges[Edges.DOWN_RIGHT]:
                do_moves([
                    Position.RIGHT.double_clockwise(),
                    Position.UP.counter_clockwise(),
                    Position.RIGHT.double_clockwise(),
                ])
            elif bad_edges[Edges.FRONT_LEFT]:
                do_moves([
                    Position.LEFT.counter_clockwise(),
                    Position.UP.clockwise(),
                    Position.LEFT.clockwise(),
                ])
            elif bad_edges[Edges.DOWN_LEFT]:
                do_moves([
                    Position.LEFT.double_clockwise(),
                    Position.UP.clockwise(),
                    Position.LEFT.double_clockwise(),
                ])
            bad_edges = eo_detection()
        if not bad_edges[Edges.DOWN_BACK]:
            if bad_edges[Edges.DOWN_RIGHT]:
                do_moves([Position.DOWN.clockwise()])
            elif bad_edges[Edges.DOWN_LEFT]:
                do_moves([Position.DOWN.counter_clockwise()])
            elif bad_edges[Edges.DOWN_FRONT]:
                do_moves([Position.DOWN.double_clockwise()])
            elif bad_edges[Edges.UP_FRONT]:
                do_moves([Position.FRONT.double_clockwise(), Position.DOWN.double_clockwise()])
            elif bad_edges[Edges.FRONT_RIGHT]:
                do_moves([
                    Position.RIGHT.counter_clockwise(),
                    Position.DOWN.clockwise(),
                    Position.RIGHT.clockwise(),
                ])
            elif bad_edges[Edges.UP_RIGHT]:
                do_moves([
                    Position.RIGHT.double_clockwise(),
                    Position.DOWN.clockwise(),
                    Position.RIGHT.double_clockwise(),
                ])
            elif bad_edges[Edges.FRONT_LEFT]:
                do_moves([
                    Position.LEFT.clockwise(),
                    Position.DOWN.counter_clockwise(),
                    Position.LEFT.counter_clockwise(),
                ])
            elif bad_edges[Edges.UP_LEFT]:
                do_moves([
                    Position.LEFT.double_clockwise(),
                    Position.DOWN.counter_clockwise(),
                    Position.LEFT.double_clockwise(),
                ])
            bad_edges = eo_detection()
        if not bad_edges[Edges.BACK_LEFT]:
            if bad_edges[Edges.DOWN_LEFT]:
                do_moves([Position.LEFT.clockwise()])
            elif bad_edges[Edges.UP_LEFT]:
                do_moves([Position.LEFT.counter_clockwise()])
            elif bad_edges[Edges.FRONT_LEFT]:
                do_moves([Position.LEFT.double_clockwise()])
            elif bad_edges[Edges.FRONT_RIGHT]:
                do_moves([Position.FRONT.double_clockwise(), Position.LEFT.double_clockwise()])
            elif bad_edges[Edges.UP_FRONT]:
                do_moves([
                    Position.UP.clockwise(),
                    Position.LEFT.counter_clockwise(),
                    Position.UP.counter_clockwise(),
                ])
            elif bad_edges[Edges.UP_RIGHT]:
                do_moves([
                    Position.UP.double_clockwise(),
                    Position.LEFT.counter_clockwise(),
                    Position.UP.double_clockwise(),
                ])
            elif bad_edges[Edges.DOWN_FRONT]:
                do_moves([
                    Position.DOWN.counter_clockwise(),
                    Position.LEFT.clockwise(),
                    Position.DOWN.clockwise(),
                ])
            elif bad_edges[Edges.DOWN_RIGHT]:
                do_moves([
                    Position.DOWN.double_clockwise(),
                    Position.LEFT.clockwise(),
                    Position.DOWN.double_clockwise(),
                ])
            bad_edges = eo_detection()
        if not bad_edges[Edges.BACK_RIGHT]:
            if bad_edges[Edges.UP_RIGHT]:
                do_moves([Position.RIGHT.clockwise()])
            elif bad_edges[Edges.DOWN_RIGHT]:
                do_moves([Position.RIGHT.counter_clockwise()])
            elif bad_edges[Edges.BACK_RIGHT]:
                do_moves([Position.RIGHT.double_clockwise()])
            elif bad_edges[Edges.FRONT_LEFT]:
                do_moves([Position.FRONT.double_clockwise(), Position.RIGHT.double_clockwise()])
            elif bad_edges[Edges.UP_FRONT]:
                do_moves([
                    Position.UP.counter_clockwise(),
                    Position.RIGHT.clockwise(),
                    Position.UP.clockwise(),
                ])
            elif bad_edges[Edges.UP_LEFT]:
                do_moves([
                    Position.UP.double_clockwise(),
                    Position.RIGHT.clockwise(),
                    Position.UP.double_clockwise(),
                ])
            elif bad_edges[Edges.DOWN_FRONT]:
                do_moves([
                    Position.DOWN.clockwise(),
                    Position.RIGHT.counter_clockwise(),
                    Position.DOWN.counter_clockwise(),
                ])
            elif bad_edges[Edges.DOWN_LEFT]:
                do_moves([
                    Position.DOWN.double_clockwise(),
                    Position.RIGHT.counter_clockwise(),
                    Position.DOWN.double_clockwise(),
                ])
        do_moves([Position.BACK.clockwise()])


def get_edges(rubik):
    return [
        {"edge": [rubik.up[0, 1], rubik.back[0, 1]], "bad": False},
        {"edge": [rubik.up[1, 0], rubik.left[0, 1]], "bad": False},
        {"edge": [rubik.up[1, 2], rubik.right[0, 1]], "bad": False},
        {"edge": [rubik.up[2, 1], rubik.front[0, 1]], "bad": False},
        {"edge": [rubik.down[0, 1], rubik.front[2, 1]], "bad": False},
        {"edge": [rubik.down[1, 0], rubik.left[2, 1]], "bad": False},
        {"edge": [rubik.down[1, 2], rubik.right[2, 1]], "bad": False},
        {"edge": [rubik.down[2, 1], rubik.back[2, 1]], "bad": False},
        {"edge": [rubik.front[1, 0], rubik.left[1, 2]], "bad": False},
        {"edge": [rubik.front[1, 2], rubik.right[1, 0]], "bad": False},
        {"edge": [rubik.back[1, 0], rubik.left[1, 0]], "bad": False},
        {"edge": [rubik.back[1, 2], rubik.right[1, 2]], "bad": False},
    ]
