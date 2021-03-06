import cv2
import os
import numpy as np
import time
import math
import scipy.optimize as optimize
import threading

from actor.BackgroundManager import BackgroundManager
from adt.Screenshot import Screenshot
from actor import Robot, InputManager, ScreenshotManager
from actor import Engine, StateManager, ReferenceManager, InputManager

# Function for finding the euclidean distance between two tuples representing points:
def _distance(a, b):
    return math.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))

def get_image():
    # return cv2.imread('data/samples/x4v/1552082540465.png')  # mask causing miss
    return cv2.imread('data/samples/x4v/1552082541237.png')  # mask causing miss
    # return cv2.imread('data/samples/x2/1552079474863.png')  # spray causing miss

# Used to optimize parameters:
# def _test_methods_cost(x):
#     StateManager.debug_hsv = HsvBounds(np.array([x[0], x[1], x[2]]), np.array([x[3], x[4], x[5]]))
#     StateManager.debug_canny = (x[6], x[7])
#     return _test_methods()


def _test_methods(scope=ReferenceManager.Scope.x2):
    StateManager.debug = False
    StateManager.scope = scope
    labels = tuple(open('data/labels/' + ReferenceManager.scope_string(scope) + '/labels.txt', 'r'))
    total_error = 0
    for label in labels:
        components = label.split('|')
        filename = components[0].strip()
        confidence = int(components[1])
        start_x, start_y = float(components[2]), float(components[3])
        end_x, end_y = float(components[4]), float(components[5])
        target = Engine.get_target(Screenshot(cv2.imread('data/samples/' + ReferenceManager.scope_string(scope) + '/' + filename), time.time()))
        error = 1
        # error = \
        #     min(_distance((target.x, target.y), (start_x, start_y)), _distance((target.x, target.y), (end_x, end_y)))
        image = cv2.imread('data/samples/' + ReferenceManager.scope_string(scope) + '/' + filename)
        if target.confidence < .5 or confidence == 0:
            if target.confidence < .5 and confidence == 0:
                error = 0
            elif target.confidence < .5:
                print("Gave up on " + filename)
                error = .5
            else:
                error = 0
        elif min(start_x, end_x) <= target.x <= max(start_x, end_x):  # within X bounds
            if min(start_y, end_y) <= target.y <= max(start_y, end_y):  # within Y bounds
                error = 0
        else:
            for i in [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)]:
                image[target.y + i[0], target.y + i[1]] = [0, 255, 0]
            print("Missed: " + filename)
            # cv2.imshow(filename, image)
            pass
        total_error += error
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    return total_error / len(labels)

# You must manually paint the masking areas black between steps
def _prep_mask(step=2, scope=ReferenceManager.Scope.x1o):
    scope_string = ReferenceManager.scope_string(scope)
    print(scope_string)
    if step == 1:
        image = cv2.imread("C:\\Users\\Eric\\Desktop\\" + scope_string + ".png")
        aoi = ReferenceManager.get_aoi(scope)
        image = image[aoi.y:(aoi.y + aoi.h), aoi.x:(aoi.x + aoi.w)]
        cv2.imwrite("C:\\Users\\Eric\\Desktop\\code\\legendary-aim-assist\\python\\data\\masks\\" + scope_string + "\\mask.png", image)
    elif step == 2:
        image = cv2.imread("C:\\Users\\Eric\\Desktop\\code\\legendary-aim-assist\\python\\data\\masks\\" + scope_string + "\\mask.png")
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(grey, 1, 255, cv2.THRESH_BINARY)
        cv2.imwrite("C:\\Users\\Eric\\Desktop\\code\\legendary-aim-assist\\python\\data\\masks\\" + scope_string + "\\mask.png", binary)

def main():

    print("Running tests...")
    for scope in (ReferenceManager.Scope.x1h, ReferenceManager.Scope.x2, ReferenceManager.Scope.x4v, ReferenceManager.Scope.x1t):
        print("\t\t", ReferenceManager.scope_string(scope), "=", _test_methods(scope))

    # Test the performance on labelled data:
    # Currently:
    #  x1h: 0.045454545454545456
    #  x2:  0.06190476190476191
    #  x4v: 0.125 (not enough data)
    #  x1t: 0.061224489795918366
    # #return

    # start the screenshotting thread (for data collection:
    StateManager.scope = ReferenceManager.Scope.x2
    screenshot_thread = BackgroundManager(float(1. / 1000), ScreenshotManager.update_view, [False])
    screenshot_thread.start()
    #
    # # Start the aiming thread:
    aim_thread = BackgroundManager(float(1. / 1000), Robot.act, [])
    aim_thread.start()
    #
    # start the hook thread:
    threading.Thread(target=InputManager.listen).start()

    print("Running...")

if __name__ == "__main__":
    main()
