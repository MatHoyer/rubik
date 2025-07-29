import logging
from .Position import Position, PRIME , DOUBLE
from .Rubik import Rubik
from .Color import get_colors_faces
from .Edges import Edges, get_edges, case_2_bad_edges, case_6_bad_edges, case_default_bad_edges
import numpy as np


class Resolver:
    def __init__(self, rubik: Rubik):
        self.rubik = rubik
        logging.info("Start resolving")
        self.solve_eo()
        # self.ida_star(None, g1_moves, 7, self.rubik.copy_rubik())

    def solve_eo(self):
        bad_edges = self.eo_detection()
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
                case_2_bad_edges(bad_edges, front_nb, back_nb, self.do_moves)
            case 6:
                case_6_bad_edges(bad_edges, front_nb, back_nb, self.do_moves)
            case _:
                case_default_bad_edges(bad_edges, front_nb, back_nb, self.do_moves, self.eo_detection)
        bad_edges = self.eo_detection()
        if sum(bad_edges):
            self.solve_eo()

    def eo_detection(self):
        edges = get_edges(self.rubik)
        for edge in edges:
            if edge["edge"][0] in [get_colors_faces().FRONT.left, get_colors_faces().FRONT.right]:
                edge["bad"] = True
            elif edge["edge"][0] in [get_colors_faces().FRONT.front, get_colors_faces().FRONT.back]:
                if edge["edge"][1] in [get_colors_faces().FRONT.up, get_colors_faces().FRONT.down]:
                    edge["bad"] = True
        return [edge["bad"] for edge in edges]

    def ida_star(self, first_move, moves, heuristic, rubik: Rubik):
        if len(rubik.solution) > heuristic:
            return False
        if self.rubik_goal(rubik):
            self.solution = rubik.solution
            self.rubik.solution = np.append(self.rubik.solution, self.solution)
            return True
        if first_move:
            self.do_move(first_move, rubik)
            rubik.solution = np.append(rubik.solution, first_move)
        for move in moves:
            if self.ida_star(move, moves, heuristic, rubik.copy_rubik()):
                return True
        return False

    @staticmethod
    def rubik_goal(rubik: Rubik):
        faces = [
            rubik.front, rubik.back,
            rubik.up, rubik.down,
            rubik.left, rubik.right,
        ]
        for face in faces:
            for i in range(3):
                for j in range(3):
                    if face[i, j] != face[1, 1]:
                        return False
        return True

    @staticmethod
    def do_move(move: str, rubik: Rubik):
        modifier = move[1] if len(move) == 2 else ""
        if modifier in PRIME:
            rubik.counter_clockwise_rotate(Position.get_good_position(move[0]))
        elif modifier is DOUBLE:
            rubik.double_clockwise_rotate(Position.get_good_position(move[0]))
        else:
            rubik.clockwise_rotate(Position.get_good_position(move[0]))

    def do_moves(self, moves: list[str]):
        for move in moves:
            modifier = move[1] if len(move) == 2 else ""
            if modifier in PRIME:
                self.rubik.counter_clockwise_rotate(Position.get_good_position(move[0]))
            elif modifier is DOUBLE:
                self.rubik.double_clockwise_rotate(Position.get_good_position(move[0]))
            else:
                self.rubik.clockwise_rotate(Position.get_good_position(move[0]))
        self.rubik.solution = np.append(self.rubik.solution, moves)
