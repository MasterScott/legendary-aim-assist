import enum
import numpy as np
import cv2

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


def get_aoi(scope):
    if scope == Scope.x2:
        return AreaOfInterest(815, 480, 280, 120)
    else:
        raise Exception("Unknown scope!")


def get_hsv(scope):
    if scope == Scope.x2:
        return HsvBounds(np.array([2, 100, 80]), np.array([10, 170, 170]))
        # return HsvBounds(np.array([1, 100, 70]), np.array([10, 170, 170]))
    else:
        raise Exception("Unknown scope!")


def get_aim(scope):
    if scope == Scope.x2:
        return [145, 60]
    else:
        raise Exception("Unknown scope!")


def _image_to_mask(img):
    return cv2.inRange(img, np.array([1, 1, 1]), np.array([255, 255, 255]))


def get_mask(scope):
    if scope == Scope.x2:
        return _image_to_mask(cv2.imread('data/masks/x2/mask.png'))
    else:
        raise Exception("Unknown scope!")
