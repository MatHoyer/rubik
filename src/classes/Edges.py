

class Edges:
    UP_BACK = 0
    UP_LEFT = 1
    UP_RIGHT = 2
    UP_FRONT = 3
    DOWN_FRONT = 4
    DOWN_LEFT = 5
    DOWN_RIGHT = 6
    DOWN_BACK = 7
    FRONT_LEFT = 8
    FRONT_RIGHT = 9
    BACK_LEFT = 10
    BACK_RIGHT = 11


def get_edges(rubik):
    return [
        {"edge": [rubik.up[0, 1], rubik.back[0, 1]], "bad": False},
        {"edge": [rubik.up[1, 0], rubik.left[0, 1]], "bad": False},
        {"edge": [rubik.up[1, 2], rubik.right[0, 1]], "bad": False},
        {"edge": [rubik.up[2, 1], rubik.front[0, 1]], "bad": False},
        {"edge": [rubik.down[0, 1], rubik.front[2, 1]], "bad": False},
        {"edge": [rubik.down[1, 0], rubik.left[2, 1]], "bad": False},
        {"edge": [rubik.down[1, 2], rubik.right[2, 1]], "bad": False},
        {"edge": [rubik.down[2, 1], rubik.back[2, 1]], "bad": False},
        {"edge": [rubik.front[1, 0], rubik.left[1, 2]], "bad": False},
        {"edge": [rubik.front[1, 2], rubik.right[1, 0]], "bad": False},
        {"edge": [rubik.back[1, 0], rubik.left[1, 0]], "bad": False},
        {"edge": [rubik.back[1, 2], rubik.right[1, 2]], "bad": False},
    ]
