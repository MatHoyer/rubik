from ursina import Entity, application, invoke, curve, held_keys
from .Rubik3D import Rubik3D


class InputHandler(Entity):
    time = 1
    is_input = False
    is_mix = False

    def __init__(self, rubik3D: Rubik3D):
        super().__init__()
        self.rubik3D = rubik3D

    def input(self, key):
        if key == "escape":
            application.quit()
        if key == "space" and not self.is_input and not self.is_mix:
            self.do_mix()
        elif not self.is_input and not self.is_mix:
            match key:
                case "f":
                    self.do_front(held_keys["shift"])
                case "b":
                    self.do_back(held_keys["shift"])
                case "u":
                    self.do_top(held_keys["shift"])
                case "d":
                    self.do_bottom(held_keys["shift"])
                case "l":
                    self.do_left(held_keys["shift"])
                case "r":
                    self.do_right(held_keys["shift"])

    def do_mix(self):
        self.is_mix = True
        dictionnary = {
            "F": lambda: self.do_front(False),
            "F\'": lambda: self.do_front(True),
            "F’": lambda: self.do_front(True),
            "F2": lambda: self.do_front(False, True),
            "B": lambda: self.do_back(False),
            "B\'": lambda: self.do_back(True),
            "B’": lambda: self.do_back(True),
            "B2": lambda: self.do_back(False, True),
            "U": lambda: self.do_top(False),
            "U\'": lambda: self.do_top(True),
            "U’": lambda: self.do_top(True),
            "U2": lambda: self.do_top(False, True),
            "D": lambda: self.do_bottom(False),
            "D\'": lambda: self.do_bottom(True),
            "D’": lambda: self.do_bottom(True),
            "D2": lambda: self.do_bottom(False, True),
            "L": lambda: self.do_left(False),
            "L\'": lambda: self.do_left(True),
            "L’": lambda: self.do_left(True),
            "L2": lambda: self.do_left(False, True),
            "R": lambda: self.do_right(False),
            "R\'": lambda: self.do_right(True),
            "R’": lambda: self.do_right(True),
            "R2": lambda: self.do_right(False, True),
        }
        for i in range(len(self.rubik3D.rubik.mix)):
            invoke(dictionnary[self.rubik3D.rubik.mix[i]], delay=i * self.time)
        invoke(lambda: setattr(self, "is_mix", False), delay=len(self.rubik3D.rubik.mix))

    def do_rotate(self, type, value):
        self.rubik3D.center.animate(type, value, duration=self.time, curve=curve.in_out_expo)
        invoke(self.rubik3D.clear_rubik, delay=self.time)
        invoke(lambda: setattr(self, "is_input", False), delay=self.time)

    def do_front(self, reverse, double=False):
        self.is_input = True
        z = 0
        for y in range(3):
            for x in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action("F\'" if reverse else "F")
        if double:
            self.rubik3D.rubik.find_good_action("F\'" if reverse else "F")
        self.do_rotate("rotation_z", round(self.rubik3D.center.rotation_z) +
                       ((-90 if reverse else 90) * (2 if double else 1)))

    def do_back(self, reverse, double=False):
        self.is_input = True
        z = 2
        for y in range(3):
            for x in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action("B\'" if reverse else "B")
        if double:
            self.rubik3D.rubik.find_good_action("B\'" if reverse else "B")
        self.do_rotate("rotation_z", round(self.rubik3D.center.rotation_z) +
                       ((90 if reverse else -90) * (2 if double else 1)))

    def do_top(self, reverse, double=False):
        self.is_input = True
        y = 0
        for x in range(3):
            for z in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action("U\'" if reverse else "U")
        if double:
            self.rubik3D.rubik.find_good_action("U\'" if reverse else "U")
        self.do_rotate("rotation_y", round(self.rubik3D.center.rotation_y) +
                       ((-90 if reverse else 90) * (2 if double else 1)))

    def do_bottom(self, reverse, double=False):
        self.is_input = True
        y = 2
        for x in range(3):
            for z in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action("D\'" if reverse else "D")
        if double:
            self.rubik3D.rubik.find_good_action("D\'" if reverse else "D")
        self.do_rotate("rotation_y", round(self.rubik3D.center.rotation_y) +
                       ((90 if reverse else -90) * (2 if double else 1)))

    def do_left(self, reverse, double=False):
        self.is_input = True
        x = 0
        for z in range(3):
            for y in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action("L\'" if reverse else "L")
        if double:
            self.rubik3D.rubik.find_good_action("L\'" if reverse else "L")
        self.do_rotate("rotation_x", round(self.rubik3D.center.rotation_x) +
                       ((90 if reverse else -90) * (2 if double else 1)))

    def do_right(self, reverse, double=False):
        self.is_input = True
        x = 2
        for z in range(3):
            for y in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action("R\'" if reverse else "R")
        if double:
            self.rubik3D.rubik.find_good_action("R\'" if reverse else "R")
        self.do_rotate("rotation_x", round(self.rubik3D.center.rotation_x) +
                       ((-90 if reverse else 90) * (2 if double else 1)))
