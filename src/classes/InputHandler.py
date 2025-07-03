from ursina import Entity, application, invoke, curve, scene


class InputHandler(Entity):
    def __init__(self, cube, center):
        super().__init__()
        self.cube = cube
        self.center = center

    def input(self, key):
        if key == "escape":
            application.quit()
        elif key == "space":
            actions = [self.do_front, self.do_back, self.do_right]
            actions[0]()
            for i in range(1, len(actions)):
                invoke(actions[i], delay=i)

    def do_rotate(self):
        self.center.animate("rotation_z", round(self.center.rotation_z) + 360, duration=1, curve=curve.in_out_expo)
        invoke(self.detach_cube, delay=1)

    def detach_cube(self):
        print("DETACH")
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    self.cube[x, y, z].world_parent = scene

    def do_front(self):
        print("FRONT")
        z = 0
        for y in range(3):
            for x in range(3):
                    self.cube[x, y, z].world_parent = self.center
        self.do_rotate()

    def do_back(self):
        print("BACK")
        z = 2
        for y in range(3):
            for x in range(3):
                    self.cube[x, y, z].world_parent = self.center
        self.do_rotate()

    def do_right(self):
        print("RIGHT")
        x = 2
        for y in range(3):
            for z in range(3):
                    self.cube[x, y, z].world_parent = self.center
        self.do_rotate()
