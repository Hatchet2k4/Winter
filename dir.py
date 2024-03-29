# Way more bothersome than it ought to be. -_-;

# directions
(LEFT,
 RIGHT,
 UP,
 DOWN,
 UPLEFT,
 UPRIGHT,
 DOWNLEFT,
 DOWNRIGHT,
 NOTHING) = range(9) # coincides with ika's internal direction constants

toStr = 'LEFT RIGHT UP DOWN UPLEFT UPRIGHT DOWNLEFT DOWNRIGHT NOTHING'.split()


# x/y displacements for each direction
delta = [
    (-1, 0),
    ( 1, 0),
    ( 0,-1),
    ( 0, 1),
    (-1,-1),
    ( 1,-1),
    (-1, 1),
    ( 1, 1),
    ( 0, 0)
    ]

# opposite directions
invert = [
    RIGHT,
    LEFT,
    DOWN,
    UP,
    DOWNRIGHT,
    DOWNLEFT,
    UPRIGHT,
    DOWNLEFT,
    NOTHING
    ]


rotateCounterCW = [ #rotate 90 degrees left
DOWN,
UP,
LEFT,
RIGHT,
DOWNLEFT,
UPLEFT,
DOWNRIGHT,
UPRIGHT
]

rotateCounterCW45 = [ #rotate 45 degrees left
DOWNLEFT,
UPRIGHT,
UPLEFT,
DOWNRIGHT,
LEFT,
UP,
DOWN,
RIGHT
]

rotateCW = [ #rotate 90 degrees right
UP,
DOWN,
RIGHT,
LEFT,
UPRIGHT,
DOWNRIGHT,
UPLEFT,
DOWNLEFT
]

rotateCW45 = [ #rotate 45 degrees right
UPLEFT,
DOWNRIGHT,
UPRIGHT,
DOWNLEFT,
UP,
RIGHT,
LEFT,
DOWN
]

invertX = [
    RIGHT,
    LEFT,
    UP,
    DOWN,
    UPRIGHT,
    UPLEFT,
    DOWNRIGHT,
    DOWNLEFT
]

invertY = [
    LEFT,
    RIGHT,
    DOWN,
    UP,
    DOWNLEFT,
    DOWNRIGHT,
    UPLEFT,
    UPRIGHT
]

def fromDelta(dx, dy):
    # -_-;

    if dy == 0:
        if dx > 0:      return RIGHT
        else:           return LEFT
    elif dx == 0:
        if dy > 0:      return DOWN
        else:           return UP
    else:
        m = abs(float(dy) / dx)
        if m > 0.8: d = DOWN
        elif m > 0.2: d = DOWNRIGHT
        else: d = RIGHT

        if dx < 0:      d = invertX[d]
        if dy < 0:      d = invertY[d]
        return d
