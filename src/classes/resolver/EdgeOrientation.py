from typing import List, Callable
from ..Color import get_colors_faces
from ..Edges import Edges, get_edges
from ..Position import Position


class EdgeOrientation:
    @staticmethod
    def edge_orientation(do_moves: Callable, eo_detection: Callable):
        bad_edges = eo_detection()
        front_nb = sum([
            bad_edges[Edges.UP_FRONT],
            bad_edges[Edges.DOWN_FRONT],
            bad_edges[Edges.FRONT_LEFT],
            bad_edges[Edges.FRONT_RIGHT],
        ])
        back_nb = sum([
            bad_edges[Edges.UP_BACK],
            bad_edges[Edges.DOWN_BACK],
            bad_edges[Edges.BACK_LEFT],
            bad_edges[Edges.BACK_RIGHT],
        ])
        match sum(bad_edges):
            case 0:
                return
            case 2:
                EdgeOrientation.augment_bad_edges(
                    bad_edges=bad_edges,
                    front_nb=front_nb,
                    back_nb=back_nb,
                    do_moves=do_moves,
                )
            case 6:
                EdgeOrientation.reduce_bad_edges(
                    bad_edges=bad_edges,
                    front_nb=front_nb,
                    back_nb=back_nb,
                    do_moves=do_moves,
                )
            case _:
                EdgeOrientation.resolve_4_bad_edges(
                    bad_edges=bad_edges,
                    front_nb=front_nb,
                    back_nb=back_nb,
                    do_moves=do_moves,
                    eo_detection=eo_detection,
                )
        bad_edges = eo_detection()
        if sum(bad_edges):
            EdgeOrientation.edge_orientation(do_moves, eo_detection)

    @staticmethod
    def eo_detection(self):
        edges = get_edges(self.rubik)
        bad_edges = []
        for edge in edges:
            if edge["edge"][0] in [get_colors_faces().FRONT.left, get_colors_faces().FRONT.right]:
                bad_edges.append(True)
            elif edge["edge"][0] in [get_colors_faces().FRONT.front, get_colors_faces().FRONT.back]:
                if edge["edge"][1] in [get_colors_faces().FRONT.up, get_colors_faces().FRONT.down]:
                    bad_edges.append(True)
                else:
                    bad_edges.append(False)
            else:
                bad_edges.append(False)
        return bad_edges

    @staticmethod
    def augment_bad_edges(bad_edges: List[int], front_nb: int, back_nb: int, do_moves: Callable):
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

    @staticmethod
    def reduce_bad_edges(bad_edges: List[int], front_nb: int, back_nb: int, do_moves: Callable):
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

    @staticmethod
    def resolve_4_bad_edges(bad_edges: List[int], front_nb: int, back_nb: int, do_moves: Callable, eo_detection):
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
