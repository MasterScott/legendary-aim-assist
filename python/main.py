import cv2
import numpy as np
import time
import math

from actor.ReferenceManager import Scope
from actor.BackgroundManager import BackgroundManager
from adt.Screenshot import Screenshot
from actor import Robot
from adt.Target import Target
from actor import ReferenceManager, ScreenshotManager, Engine

# Function for finding the euclidean distance between two tuples representing points:
def _distance(a, b):
    return math.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))

# Method used to debug by pulling in an example image:
def get_image():
    return cv2.imread('out/1551643714397.png')  # clean sample
    # return cv2.imread('out/1551643715076.png')  # occluded sample
    # return cv2.imread('out/1551643723461.png')  # very close
    # return cv2.imread('out/1551644022774.png')  # moderately far
    # return cv2.imread('out/1551644025498.png') # noisy
    # return cv2.imread('out/1551644032348.png')  # noisy
    # return cv2.imread('out/1551644036303.png')  # noisy
    # return cv2.imread('out/1551644037278.png')  # hit marker
    # return cv2.imread('out/1551643714966.png')  # also occluded
    # return cv2.imread('out/1551643723862.png')  # smoky
    # return cv2.imread('out/1551644032232.png')  # trail
    # return cv2.imread('out/1551644032600.png')  # trail
    # return cv2.imread('out/1551644033718.png')  # flash

# dictionary used to debug by backtesting a number of images:
examples = {
        'out/1551643714397.png': (180, 30),
        'out/1551643715076.png': (110, 60),
        'out/1551643723461.png': (140, 10),
        'out/1551644022774.png': (200, 10),
        'out/1551644025498.png': (82, 42),
        'out/1551644032348.png': (189, 37),
        'out/1551644036303.png': (183, 47),
        'out/1551644037278.png': (136, 37),
    }

def main():

    # start the screenshotting thread:
    screenshotThread = BackgroundManager(float(1. / 1000), ScreenshotManager.get_screenshot, [Scope.x2])
    screenshotThread.start()

    # start the hook thread::
    # threading.Thread(target=InputManager.listen).start()

    # Invoke this for debug purposes
    target = Engine.get_target(Screenshot(get_image(), time.time()))

    print("pre move")
    Robot.click(target.x, target.y)
    print("post move")

    print("Running...")

if __name__ == "__main__":
    main()
