from ursina import Entity, application, invoke, curve, held_keys
from typing import List
from .Rubik3D import Rubik3D
from .Position import PRIME, DOUBLE
from .globals import ANIMATION_TIME


class InputHandler(Entity):
    is_input = False
    is_mix = False

    def __init__(self, rubik3D: Rubik3D):
        super().__init__()
        self.rubik3D = rubik3D

    def input(self, key):
        if key == "escape":
            application.quit()
        if key == "space" and not self.is_input and not self.is_mix:
            if self.rubik3D.progression.step == 0:
                self.do_mix(self.rubik3D.rubik.mix)
            elif self.rubik3D.progression.step == 1:
                self.do_mix(self.rubik3D.rubik.solution)
        elif not self.is_input and not self.is_mix:
            match key:
                case "f":
                    self.do_front(held_keys["shift"])
                case "b":
                    self.do_back(held_keys["shift"])
                case "u":
                    self.do_up(held_keys["shift"])
                case "d":
                    self.do_down(held_keys["shift"])
                case "l":
                    self.do_left(held_keys["shift"])
                case "r":
                    self.do_right(held_keys["shift"])

    def do_mix(self, mix: List[str]):
        self.is_mix = True
        self.rubik3D.progression.next_step(len(mix))
        func_dict = {
            "F": self.do_front,
            "B": self.do_back,
            "U": self.do_up,
            "D": self.do_down,
            "L": self.do_left,
            "R": self.do_right,
        }
        for i in range(len(mix)):
            func = func_dict[mix[i][0]]
            counter = False
            double = False
            if len(mix[i]) == 2:
                counter = True if mix[i][1] in PRIME else False
                double = True if mix[i][1] is DOUBLE else False
            invoke(func, counter, double, delay=i * ANIMATION_TIME)
        invoke(lambda: setattr(self, "is_mix", False), delay=len(mix) * ANIMATION_TIME)

    def do_rotate(self, type, value):
        self.rubik3D.center.animate(type, value, duration=ANIMATION_TIME, curve=curve.in_out_expo)
        invoke(self.rubik3D.clear_rubik, delay=ANIMATION_TIME)
        invoke(lambda: setattr(self, "is_input", False), delay=ANIMATION_TIME)

    def do_front(self, counter, double=False):
        self.is_input = True
        z = 0
        for y in range(3):
            for x in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action(("F" if not counter else "F\'") if not double else "F2")
        self.do_rotate("rotation_z", round(self.rubik3D.center.rotation_z) +
                       ((-90 if counter else 90) * (2 if double else 1)))

    def do_back(self, counter, double=False):
        self.is_input = True
        z = 2
        for y in range(3):
            for x in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action(("B" if not counter else "B\'") if not double else "B2")
        self.do_rotate("rotation_z", round(self.rubik3D.center.rotation_z) +
                       ((90 if counter else -90) * (2 if double else 1)))

    def do_up(self, counter, double=False):
        self.is_input = True
        y = 0
        for x in range(3):
            for z in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action(("U" if not counter else "U\'") if not double else "U2")
        self.do_rotate("rotation_y", round(self.rubik3D.center.rotation_y) +
                       ((-90 if counter else 90) * (2 if double else 1)))

    def do_down(self, counter, double=False):
        self.is_input = True
        y = 2
        for x in range(3):
            for z in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action(("D" if not counter else "D\'") if not double else "D2")
        self.do_rotate("rotation_y", round(self.rubik3D.center.rotation_y) +
                       ((90 if counter else -90) * (2 if double else 1)))

    def do_left(self, counter, double=False):
        self.is_input = True
        x = 0
        for z in range(3):
            for y in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action(("L" if not counter else "L\'") if not double else "L2")
        self.do_rotate("rotation_x", round(self.rubik3D.center.rotation_x) +
                       ((90 if counter else -90) * (2 if double else 1)))

    def do_right(self, counter, double=False):
        self.is_input = True
        x = 2
        for z in range(3):
            for y in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action(("R" if not counter else "R\'") if not double else "R2")
        self.do_rotate("rotation_x", round(self.rubik3D.center.rotation_x) +
                       ((-90 if counter else 90) * (2 if double else 1)))
