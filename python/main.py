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
    # return cv2.imread('data/samples/x2data/samples/x2/1551643715076.png')  # occluded
    # return cv2.imread('data/samples/x2/1551643723461.png')  # very close
    # return cv2.imread('data/samples/x2/1551644022774.png')  # moderately far
    # return cv2.imread('data/samples/x2/1551644025498.png')  # noisy
    # return cv2.imread('data/samples/x2/1551644032348.png')  # noisy
    # return cv2.imread('data/samples/x2/1551644036303.png')  # noisy
    # return cv2.imread('data/samples/x2/1551644037278.png')  # hit marker
    # return cv2.imread('data/samples/x2/1551643714966.png')  # also occluded
    # return cv2.imread('data/samples/x2/1551643723862.png')  # smoky
    # return cv2.imread('data/samples/x2/1551644032232.png')  # trail
    # return cv2.imread('data/samples/x2/1551644032600.png')  # trail
    # return cv2.imread('data/samples/x2/1551644033718.png')  # flash
    # return cv2.imread('data/samples/x2/1551643710602.png')  # crawl
    # return cv2.imread('data/samples/x2/1551643714726.png')  # occluded
    # return cv2.imread('data/samples/x2/1551643716105.png')  # mirage # fails, but understandably
    # return cv2.imread('data/samples/x2/1551643723862.png') # close, flash
    # return cv2.imread('data/samples/x2/1551643724589.png')  # heavy occlusion

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

# # You must manually paint the masking areas black between steps
# def _prep_mask(step=2, scope=ReferenceManager.Scope.x4v):
#     scope_string = ReferenceManager.scope_string(scope)
#     if step == 1:
#         image = cv2.imread("C:\\Users\\Eric\\Desktop\\" + scope_string + ".png")
#         aoi = ReferenceManager.get_aoi(scope)
#         image = image[aoi.y:(aoi.y + aoi.h), aoi.x:(aoi.x + aoi.w)]
#         cv2.imwrite("C:\\Users\\Eric\\Desktop\\code\\legendary-aim-assist\\python\\data\\masks\\" + scope_string + "\\mask.png", image)
#     elif step == 2:
#         image = cv2.imread("C:\\Users\\Eric\\Desktop\\code\\legendary-aim-assist\\python\\data\\masks\\" + scope_string + "\\mask.png")
#         grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         _, binary = cv2.threshold(grey, 1, 255, cv2.THRESH_BINARY)
#         cv2.imwrite("C:\\Users\\Eric\\Desktop\\code\\legendary-aim-assist\\python\\data\\masks\\" + scope_string + "\\mask.png", binary)

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
