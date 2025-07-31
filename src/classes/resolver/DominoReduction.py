from typing import List, Callable
from ..Position import Position
from ..Edges import Edges


class DominoReduction():
    @staticmethod
    def domino_reduction(do_moves: Callable, e_slice_detection: Callable):
        DominoReduction.balance_edges(do_moves, e_slice_detection)
        DominoReduction.e_slice_orientation(do_moves, e_slice_detection)

    @staticmethod
    def balance_edges(do_moves: Callable, e_slice_detection: Callable):
        bad_edges = e_slice_detection()
        up_nb = sum([
            bad_edges[Edges.UP_BACK],
            bad_edges[Edges.UP_LEFT],
            bad_edges[Edges.UP_RIGHT],
            bad_edges[Edges.UP_FRONT],
        ])
        down_nb = sum([
            bad_edges[Edges.DOWN_FRONT],
            bad_edges[Edges.DOWN_LEFT],
            bad_edges[Edges.DOWN_RIGHT],
            bad_edges[Edges.DOWN_BACK],
        ])
        if up_nb - 1 <= down_nb <= up_nb + 1:
            return
        if up_nb > down_nb:
            if bad_edges[Edges.UP_LEFT] and not bad_edges[Edges.DOWN_LEFT]:
                do_moves([Position.LEFT.double_clockwise()])
            elif bad_edges[Edges.UP_RIGHT] and not bad_edges[Edges.DOWN_RIGHT]:
                do_moves([Position.RIGHT.double_clockwise()])
            else:
                do_moves([Position.UP.clockwise(), Position.LEFT.double_clockwise()])
        else:
            if bad_edges[Edges.DOWN_LEFT] and not bad_edges[Edges.UP_LEFT]:
                do_moves([Position.LEFT.double_clockwise()])
            elif bad_edges[Edges.DOWN_RIGHT] and not bad_edges[Edges.UP_RIGHT]:
                do_moves([Position.RIGHT.double_clockwise()])
            else:
                do_moves([Position.DOWN.clockwise(), Position.LEFT.double_clockwise()])
        DominoReduction.balance_edges(do_moves, e_slice_detection)

    @staticmethod
    def e_slice_orientation(do_moves: Callable, e_slice_detection: Callable):
        bad_edges = e_slice_detection()
        print(sum(bad_edges))
        up_nb = sum([
            bad_edges[Edges.UP_BACK],
            bad_edges[Edges.UP_LEFT],
            bad_edges[Edges.UP_RIGHT],
            bad_edges[Edges.UP_FRONT],
        ])
        down_nb = sum([
            bad_edges[Edges.DOWN_FRONT],
            bad_edges[Edges.DOWN_LEFT],
            bad_edges[Edges.DOWN_RIGHT],
            bad_edges[Edges.DOWN_BACK],
        ])
        match sum(bad_edges):
            case 0:
                return
            case 2:
                pass
            case 6:
                DominoReduction.reduce_bad_edges(
                    bad_edges=bad_edges,
                    up_nb=up_nb,
                    down_nb=down_nb,
                    do_moves=do_moves,
                )
            case _:
                pass
        bad_edges = e_slice_detection()
        print(sum(bad_edges))
        # if sum(bad_edges):
        #     Domino.e_slice_orientation()

    @staticmethod
    def reduce_bad_edges(bad_edges: List[int], up_nb: int, down_nb: int, do_moves: Callable):
        if not bad_edges[Edges.FRONT_LEFT] or not bad_edges[Edges.BACK_LEFT]:
            if not bad_edges[Edges.UP_LEFT]:
                if bad_edges[Edges.UP_FRONT]:
                    do_moves([Position.UP.clockwise()])
                elif bad_edges[Edges.UP_BACK]:
                    do_moves([Position.UP.counter_clockwise()])
                else:
                    do_moves([Position.UP.double_clockwise()])
            if not bad_edges[Edges.DOWN_LEFT]:
                if bad_edges[Edges.DOWN_FRONT]:
                    do_moves([Position.DOWN.counter_clockwise()])
                elif bad_edges[Edges.DOWN_BACK]:
                    do_moves([Position.DOWN.clockwise()])
                else:
                    do_moves([Position.DOWN.double_clockwise()])
            if bad_edges[Edges.FRONT_LEFT]:
                if up_nb > down_nb:
                    do_moves([Position.LEFT.counter_clockwise()])
                else:
                    do_moves([Position.LEFT.clockwise()])
            else:
                if up_nb > down_nb:
                    do_moves([Position.LEFT.clockwise()])
                else:
                    do_moves([Position.LEFT.counter_clockwise()])
        else:
            if not bad_edges[Edges.UP_RIGHT]:
                if bad_edges[Edges.UP_FRONT]:
                    do_moves([Position.UP.counter_clockwise()])
                elif bad_edges[Edges.UP_BACK]:
                    do_moves([Position.UP.clockwise()])
                else:
                    do_moves([Position.UP.double_clockwise()])
            if not bad_edges[Edges.DOWN_RIGHT]:
                if bad_edges[Edges.DOWN_FRONT]:
                    do_moves([Position.DOWN.clockwise()])
                elif bad_edges[Edges.DOWN_BACK]:
                    do_moves([Position.DOWN.counter_clockwise()])
                else:
                    do_moves([Position.DOWN.double_clockwise()])
            if bad_edges[Edges.FRONT_RIGHT]:
                if up_nb > down_nb:
                    do_moves([Position.RIGHT.clockwise()])
                else:
                    do_moves([Position.RIGHT.counter_clockwise()])
            else:
                if up_nb > down_nb:
                    do_moves([Position.RIGHT.counter_clockwise()])
                else:
                    do_moves([Position.RIGHT.clockwise()])
