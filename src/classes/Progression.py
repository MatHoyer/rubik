from ursina import Entity, Text, color, camera, invoke
from .globals import ANIMATION_TIME


class Progression():
    step = 0
    height = .05
    width = .65

    def __init__(self):
        Entity(
            model="quad",
            position=(0, .4, 0),
            scale=(
                  self.width + .01,
                  self.height + .01,
            ),
            color=color.black,
            parent=camera.ui,
            z=2,
        )
        Entity(
            model="quad",
            position=(0, .4, 0),
            scale=(
                 self.width,
                 self.height
            ),
            color=color.red,
            parent=camera.ui,
            z=1,
        )
        self.progress_bar = Entity(
            model="quad",
            position=(-self.width / 2, .4, 0),
            origin=(-.5, 0),
            scale=(self.width, self.height),
            color=color.green,
            parent=camera.ui,
            scale_x=0,
        )
        Text("Initial", position=(-.4, .4, 0), origin=(0, 0))
        Text("Mixed", position=(0, .45, 0), origin=(0, 0))
        Text("Resolved", position=(.4, .4, 0), origin=(0, 0))
        Text("Press 'Space' for next step", position=(0, .35, 0), origin=(0, 0))

    def next_step(self, mixLen):
        self.step += 1
        if self.step == 1 or self.step == 2:
            for i in range(mixLen):
                invoke(self.inc, self.width / 2 / mixLen, delay=i * ANIMATION_TIME)

    def inc(self, a):
        self.progress_bar.scale_x += a
