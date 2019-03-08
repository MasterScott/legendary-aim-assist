import enum
import numpy as np
import cv2

from actor import StateManager


def scope_string(scope):
    return str(scope)[len('Scope.'):]

class Scope(enum.Enum):
    x1h = 1
    x1t = 2
    x2 = 3
    x2v = 4
    x4v = 5


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
    def __str__(self):
        return str(str(self.lower) + "," + str(self.upper))


def get_aoi(scope):
    if scope == Scope.x1h:
        return AreaOfInterest(881, 479, 161, 100)
    if scope == Scope.x1t:
        return AreaOfInterest(888, 485, 147, 112)
    elif scope == Scope.x2:
        return AreaOfInterest(815, 456, 292, 173)
    elif scope == Scope.x2v or scope == Scope.x4v:
        return AreaOfInterest(715, 300, 485, 488)
    else:
        raise Exception("Unknown scope!")


def get_hsv(scope):
    if scope in key_dict().values() and scope not in [Scope.x1t]: # TODO determine the colors for the x1t scope
        return HsvBounds(np.array([1, 50, 60]), np.array([10, 180, 190]))
    else:
        raise Exception("Unknown scope!")


def get_aim(scope):
    aoi = get_aoi(scope)
    return [960 - aoi.x, 539 - aoi.y]

def _image_to_mask(img):
    return cv2.inRange(img, np.array([1, 1, 1]), np.array([255, 255, 255]))


_mask_cache = dict()
def get_mask(scope):
    if scope not in _mask_cache:
        if scope in key_dict().values():
            _mask_cache[scope] = _image_to_mask(cv2.imread('data/masks/' + scope_string(scope) + '/mask.png'))
        else:
            raise Exception("Unknown scope!")
    return _mask_cache[scope]

def key_dict():
    return {
        StateManager.x2_key:  Scope.x2,
        StateManager.x1h_key: Scope.x1h,
        StateManager.x1t_key: Scope.x1t,
        StateManager.x4v_key: Scope.x4v
    }

