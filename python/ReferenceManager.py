import enum
import numpy as np

def scope_string(scope):
    return scope[len('Scope.'):]

class Scope(enum.Enum):
    x2 = 1


class AreaOfInterest:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class HsvBounds:
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

# TODO
def get_aoi(type):
    if type == Scope.x2:
        return AreaOfInterest(815, 480, 280, 120)
    else:
        raise Exception("Unknown scope!")

def get_hsv(type):
    if type == Scope.x2:
        return HsvBounds(np.array([1, 100, 70]), np.array([10, 170, 170]))
    else:
        raise Exception("Unknown scope!")

def get_aim(type):
    if type == Scope.x2:
        return [145, 60]
    else:
        raise Exception("Unknown scope!")
