from ursina import Entity, application, invoke, curve
from .Rubik3D import Rubik3D


class InputHandler(Entity):
    def __init__(self, rubik3D: Rubik3D):
        super().__init__()
        self.rubik3D = rubik3D

    def input(self, key):
        if key == "escape":
            application.quit()
        elif key == "space":
            actions = [self.do_front]
            for i in range(len(actions)):
                invoke(actions[i], delay=i)

    def do_rotate(self, type, value):
        self.rubik3D.center.animate(type, value, duration=1, curve=curve.in_out_expo)
        invoke(self.rubik3D.clear_rubik, delay=1)

    def do_front(self):
        print("FRONT")
        z = 0
        for y in range(3):
            for x in range(3):
                self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
        self.do_rotate("rotation_z", round(self.rubik3D.center.rotation_z) + 90)

    # def do_back(self):
    #     print("BACK")
    #     z = 2
    #     for y in range(3):
    #         for x in range(3):
    #             self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
    #     self.do_rotate("rotation_z", round(self.rubik3D.center.rotation_z) - 90)

    # def do_right(self):
    #     print("RIGHT")
    #     x = 2
    #     for y in range(3):
    #         for z in range(3):
    #             self.rubik3D.cube[x, y, z].color = "#FF00FF"
    #             self.rubik3D.cube[x, y, z].world_parent = self.rubik3D.center
    #     # self.do_rotate("rotation_x", round(self.center.rotation_x) + 90)
