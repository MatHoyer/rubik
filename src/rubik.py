# from ursina import *

# app = Ursina()

# cube = Entity(model='cube', color=hsv(300,1,1), scale=2, collider='box')

# def spin():
#     cube.animate('rotation_y', cube.rotation_y+360, duration=2, curve=curve.in_out_expo)

# cube.on_click = spin
# EditorCamera()  # add camera controls for orbiting and moving the camera

# app.run()

import sys
import logging
from classes.Rubik import Rubik
from classes.Color import Color
from classes.Position import Position

args = sys.argv[1:]

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s ---- %(asctime)s'
)

cube = Rubik(mix=args[0])
print(cube)
# print(cube._front)
# print(cube._front[0][0] == Color.WHITE)
# print(Color.WHITE == Color.WHITE)
# print(Position.get_positions())
# Position.get_good_position('F')

