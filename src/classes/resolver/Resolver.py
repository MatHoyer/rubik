import logging
from ..Position import Position, PRIME , DOUBLE
from ..Rubik import Rubik
from ..Color import get_colors_faces
from ..Edges import Edges, get_edges
from .EdgeOrientation import EdgeOrientation
from .DominoReduction import DominoReduction
import numpy as np


class Resolver:
    def __init__(self, rubik: Rubik):
        self.rubik = rubik
        logging.info("Start resolving")
        EdgeOrientation.edge_orientation(self.do_moves, self.eo_detection)
        DominoReduction.domino_reduction(self.do_moves, self.e_slice_detection)
        # self.ida_star(None, g1_moves, 7, self.rubik.copy_rubik())

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

    def e_slice_detection(self):
        edges = get_edges(self.rubik)
        bad_edges = []
        for edge in edges:
            if Edges.UP_BACK <= edge["face"] <= Edges.DOWN_BACK and \
                    edge["edge"][0] not in [get_colors_faces().FRONT.up, get_colors_faces().FRONT.down]:
                bad_edges.append(True)
            elif Edges.FRONT_LEFT <= edge["face"] <= Edges.BACK_RIGHT and \
                    edge["edge"][0] in [get_colors_faces().FRONT.up, get_colors_faces().FRONT.down]:
                bad_edges.append(True)
            else:
                bad_edges.append(False)
        return bad_edges

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
