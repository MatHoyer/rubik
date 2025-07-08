from ursina import Entity, Vec3, EditorCamera, destroy
from .Rubik import Rubik
from .Color import colors
from .Progression import Progression
import numpy as np


class Rubik3D:
    def __init__(self, rubik: Rubik) -> None:
        self.rubik = rubik
        self.cube = np.empty((3, 3, 3), dtype=object)
        self.set_rubik_struct()
        Entity(model='sphere', color=colors["black"], scale=2, position=Vec3(1, -1, 1))
        self.center = Entity(model='sphere', color=colors["black"], scale=1, position=Vec3(1, -1, 1))
        self.radius = .51
        self.faces = []
        self.set_faces()
        self.progression = Progression()
        EditorCamera(position=Vec3(1, -1, 1), rotation_y=-45, rotation_x=25)

    def set_rubik_struct(self):
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    self.cube[x, y, z] = Entity(model='cube', color=colors["black"],
                                                position=Vec3(x, -y, z), scale=.9)

    def set_faces(self):
        faces = self.rubik.get_faces()
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    if x == 0:
                        t = {0: 2, 1: 1, 2: 0}[z]
                        self.faces.append(Entity(
                            model='quad',
                            color=colors[faces.left[y][t]],
                            scale=.7,
                            position=Vec3(-self.radius, 0, 0),
                            rotation_y=90,
                            parent=self.cube[x, y, z]
                        ))
                    elif x == 2:
                        self.faces.append(Entity(
                            model='quad',
                            color=colors[faces.right[y][z]],
                            scale=.7,
                            position=Vec3(self.radius, 0, 0),
                            rotation_y=-90,
                            parent=self.cube[x, y, z]
                        ))
                    if y == 0:
                        t = {0: 2, 1: 1, 2: 0}[z]
                        self.faces.append(Entity(
                            model='quad',
                            color=colors[faces.top[t][x]],
                            scale=.7,
                            position=Vec3(0, self.radius, 0),
                            rotation_x=90,
                            parent=self.cube[x, y, z]
                        ))
                    elif y == 2:
                        self.faces.append(Entity(
                            model='quad',
                            color=colors[faces.bottom[z][x]],
                            scale=.7,
                            position=Vec3(0, -self.radius, 0),
                            rotation_x=-90,
                            parent=self.cube[x, y, z]
                        ))
                    if z == 0:
                        self.faces.append(Entity(
                            model='quad',
                            color=colors[faces.front[y][x]],
                            scale=.7,
                            position=Vec3(0, 0, -self.radius),
                            rotation_y=0,
                            parent=self.cube[x, y, z]
                        ))
                    elif z == 2:
                        self.faces.append(Entity(
                            model='quad',
                            color=colors[faces.back[y][x]],
                            scale=.7,
                            position=Vec3(0, 0, self.radius),
                            rotation_y=180,
                            parent=self.cube[x, y, z]
                        ))

    def clear_rubik(self):
        for i in range(len(self.faces)):
            destroy(self.faces[i])
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    destroy(self.cube[x, y, z])
        destroy(self.center)
        self.center = Entity(model='sphere', color=colors["black"], scale=1, position=Vec3(1, -1, 1))
        self.set_rubik_struct()
        self.set_faces()
