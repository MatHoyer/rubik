from ursina import Ursina, Entity, Vec3, EditorCamera, curve
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
        # self._back[1][0] = "O"
        # print(self._back)
        radius = .51
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    if z == 0:
                        Entity(model='quad', color=colors[self._front[y][x]], scale=.7, position=Vec3(0, 0, -radius), parent=cube[x, y, z])
                    elif z == 2:
                        Entity(model='quad', color=colors[self._back[y][x]], scale=.7, position=Vec3(0, 0, radius), rotation_y=180, parent=cube[x, y, z])
                    if y == 0:
                        Entity(model='quad', color=colors[self._bottom[y][x]], scale=.7, position=Vec3(0, -radius, 0), rotation_x=-90, parent=cube[x, y, z])
                    elif y == 2:
                        Entity(model='quad', color=colors[self._top[y][x]], scale=.7, position=Vec3(0, radius, 0), rotation_x=90, parent=cube[x, y, z])
                    if x == 0:
                        Entity(model='quad', color=colors[self._left[y][x]], scale=.7, position=Vec3(-radius, 0, 0), rotation_y=90, parent=cube[x, y, z])
                    elif x == 2:
                        Entity(model='quad', color=colors[self._right[y][x]], scale=.7, position=Vec3(radius, 0, 0), rotation_y=-90, parent=cube[x, y, z])
        # yellow = [0,0,0,0,0,0,0,0,0]
        # blue = [0,0,0,0,0,0,0,0,0]
        # green = [0,0,0,0,0,0,0,0,0]
        # yellow[0] = Entity(model='quad', color=colors["yellow"], scale=.7, position=Vec3(-1, 1, -1.46))
        # blue[6] = Entity(model='quad', color=colors["blue"], scale=.7, position=Vec3(-1, 1.46, -1), rotation_x=90)
        # green[2] = Entity(model='quad', color=colors["green"], scale=.7, position=Vec3(-1.46, 1, -1), rotation_y=90)

        cube_test = Entity()
        cube[0][0][0].parent = cube_test
        cube[1][0][0].parent = cube_test
        cube[2][0][0].parent = cube_test

        cube[0][1][0].parent = cube_test
        cube[1][1][0].parent = cube_test
        cube[2][1][0].parent = cube_test

        cube[0][2][0].parent = cube_test
        cube[1][2][0].parent = cube_test
        cube[2][2][0].parent = cube_test

        cube_test.animate("rotation_z", round(cube_test.rotation_z) + 360, duration=5, curve=curve.in_out_expo)

        EditorCamera()
        self.app.run()
