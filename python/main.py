import cv2
import numpy as np
import time
import math
import scipy.optimize as optimize
import threading

from actor.BackgroundManager import BackgroundManager
from adt.Screenshot import Screenshot
from actor import Robot, InputManager
from actor import ScreenshotManager, Engine, StateManager, ReferenceManager

# Function for finding the euclidean distance between two tuples representing points:
def _distance(a, b):
    return math.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))

def get_image():
    return cv2.imread('data/samples/x2/1551643714397.png')  # clean sample

# Used to optimize parameters:
# def _test_methods_cost(x):
#     StateManager.debug_hsv = HsvBounds(np.array([x[0], x[1], x[2]]), np.array([x[3], x[4], x[5]]))
#     StateManager.debug_canny = (x[6], x[7])
#     return _test_methods()


def _test_methods():
    labels = tuple(open('data/labels/x2/labels.txt', 'r'))
    total_error = 0
    for label in labels:
        components = label.split('|')
        filename = components[0].strip()
        start_x, start_y = float(components[1]), float(components[2])
        end_x, end_y = float(components[3]), float(components[4])
        target = Engine.get_target(Screenshot(cv2.imread('data/samples/x2/' + filename), time.time()))
        error = 1
        # error = \
        #     min(_distance((target.x, target.y), (start_x, start_y)), _distance((target.x, target.y), (end_x, end_y)))
        if target.confidence < .5:
            error = .5
        elif min(start_x, end_x) <= target.x <= max(start_x, end_x):  # within X bounds
            if min(start_y, end_y) <= target.y <= max(start_y, end_y):  # within Y bounds
                error = 0
        else:
            image = cv2.imread('data/samples/x2/' + filename)
            for i in [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)]:
                image[target.y + i[0], target.y + i[1]] = [0, 255, 0]
            # print(filename)
            # cv2.imshow(filename, image)
            # cv2.waitKey(0)
            cv2.destroyAllWindows()
            pass
        total_error += error
    return total_error / len(labels)

def main():

    # Test the performance on labelled data:
    print(_test_methods())  # currently ~25% miss rate
    # #return
    #
    # # start the screenshotting thread (for data collection:
    # screenshot_thread = BackgroundManager(float(1. / 1000), ScreenshotManager.update_view, [])
    # screenshot_thread.start()
    #
    # # Start the aiming thread:
    # aim_thread = BackgroundManager(float(1. / 1000), Robot.act, [])
    # aim_thread.start()
    #
    # # start the hook thread:
    # threading.Thread(target=InputManager.listen).start()
    #
    # # Invoke this for debug purposes
    # target = Engine.get_target(Screenshot(get_image(), time.time()))

    # Normally, this would be invoked by the Engine itself
    # Robot.move(target.x, target.y)

    print("Running...")

if __name__ == "__main__":
    main()
