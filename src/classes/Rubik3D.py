from ursina import Ursina, Entity, Vec3, EditorCamera, curve, scene
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
                                           position=Vec3(x, -y, z), scale=.9)

        Entity(model='sphere', color=colors["black"], scale=2, position=Vec3(1, -1, 1))
        center = Entity(model='sphere', color=colors["black"], scale=1, position=Vec3(1, -1, 1))
        # HELPER ------------------------------------------------------------------------------------------
        axes = Entity()
        Entity(model='cube', color=colors[Color.RED], scale=1, position=Vec3(7, -1, 1), parent=axes)
        Entity(model='cube', color=colors[Color.GREEN], scale=1, position=Vec3(1, 5, 1), parent=axes)
        Entity(model='cube', color=colors[Color.BLUE], scale=1, position=Vec3(1, -1, 7), parent=axes)
        # -------------------------------------------------------------------------------------------------
        radius = .51
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    if x == 0:
                        t = {0: 2, 1: 1, 2: 0}[z]
                        Entity(model='quad', color=colors[self._left[y][t]], scale=.7, position=Vec3(-radius, 0, 0), rotation_y=90, parent=cube[x, y, z])
                    elif x == 2:
                        Entity(model='quad', color=colors[self._right[y][z]], scale=.7, position=Vec3(radius, 0, 0), rotation_y=-90, parent=cube[x, y, z])
                    if y == 0:
                        t = {0: 2, 1: 1, 2: 0}[z]
                        Entity(model='quad', color=colors[self._top[t][x]], scale=.7, position=Vec3(0, radius, 0), rotation_x=90, parent=cube[x, y, z])
                    elif y == 2:
                        Entity(model='quad', color=colors[self._bottom[z][x]], scale=.7, position=Vec3(0, -radius, 0), rotation_x=-90, parent=cube[x, y, z])
                    if z == 0:
                        Entity(model='quad', color=colors[self._front[y][x]], scale=.7, position=Vec3(0, 0, -radius), rotation_y=0, parent=cube[x, y, z])
                    elif z == 2:
                        Entity(model='quad', color=colors[self._back[y][x]], scale=.7, position=Vec3(0, 0, radius), rotation_y=180, parent=cube[x, y, z])

        cube[0][0][0].world_parent = center
        cube[1][0][0].world_parent = center
        cube[2][0][0].world_parent = center

        cube[0][1][0].world_parent = center
        cube[1][1][0].world_parent = center
        cube[2][1][0].world_parent = center

        cube[0][2][0].world_parent = center
        cube[1][2][0].world_parent = center
        cube[2][2][0].world_parent = center

        center.animate("rotation_z", round(center.rotation_z) + 360, duration=5, curve=curve.in_out_expo)

        EditorCamera(position=Vec3(1, -1, 1))

    def run(self):
        self.app.run()

    def __str__(self):
        return super().__str__()

