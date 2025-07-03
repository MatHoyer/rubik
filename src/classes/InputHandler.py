from ursina import Entity, application, invoke, curve, held_keys
from .Rubik3D import Rubik3D


class InputHandler(Entity):
    time = 1

    def __init__(self, rubik3D: Rubik3D):
        super().__init__()
        self.rubik3D = rubik3D
        self.is_animated = False

    def input(self, key):
        if key == "escape":
            application.quit()
        elif not self.is_animated:
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

    def do_rotate(self, type, value):
        self.rubik3D.center.animate(type, value, duration=self.time, curve=curve.in_out_expo)
        invoke(self.rubik3D.clear_rubik, delay=self.time)
        invoke(lambda: setattr(self, "is_animated", False), delay=self.time)

    def do_front(self, reverse):
        self.is_animated = True
        z = 0
        for y in range(3):
            for x in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action("F\'" if reverse else "F")
        self.do_rotate("rotation_z", round(self.rubik3D.center.rotation_z) + (-90 if reverse else 90))

    def do_back(self, reverse):
        self.is_animated = True
        z = 2
        for y in range(3):
            for x in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action("B\'" if reverse else "B")
        self.do_rotate("rotation_z", round(self.rubik3D.center.rotation_z) + (90 if reverse else -90))

    def do_top(self, reverse):
        self.is_animated = True
        y = 0
        for x in range(3):
            for z in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action("U\'" if reverse else "U")
        self.do_rotate("rotation_y", round(self.rubik3D.center.rotation_y) + (-90 if reverse else 90))

    def do_bottom(self, reverse):
        self.is_animated = True
        y = 2
        for x in range(3):
            for z in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action("D\'" if reverse else "D")
        self.do_rotate("rotation_y", round(self.rubik3D.center.rotation_y) + (90 if reverse else -90))

    def do_left(self, reverse):
        self.is_animated = True
        x = 0
        for z in range(3):
            for y in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action("L\'" if reverse else "L")
        self.do_rotate("rotation_x", round(self.rubik3D.center.rotation_x) + (90 if reverse else -90))

    def do_right(self, reverse):
        self.is_animated = True
        x = 2
        for z in range(3):
            for y in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.rubik3D.rubik.find_good_action("R\'" if reverse else "R")
        self.do_rotate("rotation_x", round(self.rubik3D.center.rotation_x) + (-90 if reverse else 90))
