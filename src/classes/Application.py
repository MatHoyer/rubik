from ursina import Ursina

from .Rubik3D import Rubik3D
from .InputHandler import InputHandler


class Application:
    def __init__(self, rubik):
        self.app = Ursina(title="Rubik", size=[1000, 1000], development_mode=True)
        self.rubik3D = Rubik3D(rubik)
        self.input_handler = InputHandler(self.rubik3D)

    def run(self):
        self.app.run()
