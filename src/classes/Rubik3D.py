from ursina import Ursina, Entity, Vec3, EditorCamera
from .Rubik import Rubik
from .Color import Color, colors
import numpy as np


class Rubik3D(Rubik):
    def __init__(self, mix: str | int) -> None:
        super().__init__(mix)
        self.app = Ursina(title="Rubik", size=[1000, 1000])
        cube = np.empty((3, 3, 3), dtype=object)
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    cube[x, y, z] = Entity(model='cube', color=colors["black"],
                                           position=Vec3(x - 1, y - 1 , z - 1), scale=.9)

        Entity(model='sphere', color=colors["black"], scale=2)
        # HELPER ------------------------------------------------------------------------------------------
        axes = Entity()
        Entity(model='cube', color=colors[Color.RED], scale=1, position=Vec3(6, 0, 0), parent=axes)
        Entity(model='cube', color=colors[Color.GREEN], scale=1, position=Vec3(0, 6, 0), parent=axes)
        Entity(model='cube', color=colors[Color.BLUE], scale=1, position=Vec3(0, 0, 6), parent=axes)
        # -------------------------------------------------------------------------------------------------

        # axes.animate("rotation_y", axes.rotation_y+360, duration=5, curve=curve.in_out_expo)
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    print(cube[x, y, z], x, y, z)
                    if z == 0:
                        Entity(model='quad', color=colors[Color.BLUE], scale=.7, position=Vec3(x - 1, y - 1, z - 1 - .46), rotation_y=0, rotation_x=0)
                    elif z == 2:
                        Entity(model='quad', color=colors[Color.GREEN], scale=.7, position=Vec3(x - 1, y - 1, z - 1 + .46), rotation_y=180, rotation_x=0)

        # yellow = [0,0,0,0,0,0,0,0,0]
        # blue = [0,0,0,0,0,0,0,0,0]
        # green = [0,0,0,0,0,0,0,0,0]
        # yellow[0] = Entity(model='quad', color=colors["yellow"], scale=.7, position=Vec3(-1, 1, -1.46))
        # blue[6] = Entity(model='quad', color=colors["blue"], scale=.7, position=Vec3(-1, 1.46, -1), rotation_x=90)
        # green[2] = Entity(model='quad', color=colors["green"], scale=.7, position=Vec3(-1.46, 1, -1), rotation_y=90)

        # cube_test = Entity()
        # yellow[0].parent = cube_test
        # blue[6].parent = cube_test
        # green[2].parent = cube_test
        # cube[6].parent = cube_test
        # cube[7].parent = cube_test
        # cube[8].parent = cube_test

        # cube[15].parent = cube_test
        # cube[16].parent = cube_test
        # cube[17].parent = cube_test

        # cube[24].parent = cube_test
        # cube[25].parent = cube_test
        # cube[26].parent = cube_test

        # cube_test.animate("rotation_y", round(cube_test.rotation_y) + 360, duration=1, curve=curve.in_out_expo)

        EditorCamera()
        self.app.run()
