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
    # return cv2.imread('out/1551643714397.png')  # clean sample
    # return cv2.imread('out/1551643715076.png')  # occluded
    # return cv2.imread('out/1551643723461.png')  # very close
    return cv2.imread('out/1551644022774.png')  # moderately far
    # return cv2.imread('out/1551644025498.png')  # noisy
    # return cv2.imread('out/1551644032348.png')  # noisy
    # return cv2.imread('out/1551644036303.png')  # noisy
    # return cv2.imread('out/1551644037278.png')  # hit marker
    # return cv2.imread('out/1551643714966.png')  # also occluded
    # return cv2.imread('out/1551643723862.png')  # smoky
    # return cv2.imread('out/1551644032232.png')  # trail
    # return cv2.imread('out/1551644032600.png')  # trail
    # return cv2.imread('out/1551644033718.png')  # flash
    # return cv2.imread('out/1551643710602.png')  # crawl
    # return cv2.imread('out/1551643714726.png')  # occluded
    # return cv2.imread('out/1551643716105.png')  # mirage # fails, but understandably
    # return cv2.imread('out/1551643723862.png') # close, flash
    # return cv2.imread('out/1551643724589.png')  # heavy occlusion

def _test_methods():

    labels = tuple(open('data/labels/x2/labels.txt', 'r'))
    print(labels)

    total_error = 0
    for label in labels:
        components = label.split('|')
        filename = components[0]
        start_x, start_y = float(components[1]), float(components[2])
        end_x, end_y = float(components[3]), float(components[4])
        target = Engine.get_target(Screenshot(cv2.imread('data/labels/x2/' + filename), time.time()))
        error = min(_distance(target, (start_x, start_y)), _distance(target, (end_x, end_y)))
        if target.x <= max(start_x, end_x) and target >= min(start_x, end_x): # within X bounds
            if target.y <= max(start_y, end_y) and target >= min(start_y, end_y): # within Y bounds
                error = 0
        total_error += (error ** 2)

    return math.sqrt(total_error)


def main():

    print(_test_methods())
    return

    # start the screenshotting thread:
    screenshotThread = BackgroundManager(float(1. / 1000), ScreenshotManager.get_screenshot, [StateManager.scope])
    screenshotThread.start()

    # start the hook thread::
    # threading.Thread(target=InputManager.listen).start()

    # Invoke this for debug purposes
    target = Engine.get_target(Screenshot(get_image(), time.time()))

    # Normally, this would be invoked by the Engine itself
    Robot.click(target.x, target.y)

    print("Running...")

if __name__ == "__main__":
    main()
