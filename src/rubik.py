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

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s ---- %(asctime)s'
)

if __name__ == "__main__":
    args = sys.argv[1:]
    mix = None
    if len(args) == 1:
        mix = sys.argv[0]
        try:
            mix = int(mix)
        except Exception:
            logging.info('Mix profided')

    cube = Rubik(mix=mix)
    print(cube)
