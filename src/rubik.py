# from ursina import *

# app = Ursina()

# cube = Entity(model='cube', color=hsv(300,1,1), scale=2, collider='box')

# def spin():
#     cube.animate('rotation_y', cube.rotation_y+360, duration=2, curve=curve.in_out_expo)

# cube.on_click = spin
# EditorCamera()  # add camera controls for orbiting and moving the camera

# app.run()

from classes.Rubik import Rubik
from classes.Color import Color

cube = Rubik(mix='')
print(cube._front)
print(cube._front[0][0] == Color.WHITE)
print(Color.WHITE == Color.WHITE)

