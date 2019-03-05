import cv2
import numpy as np
import time
import math

from actor.ReferenceManager import Scope
from actor.BackgroundManager import BackgroundManager
from adt.Screenshot import Screenshot
from adt.Target import Target
from actor import ReferenceManager, ScreenshotManager


# Function for finding the euclidean distance between two tuples representing points:
def distance(a, b):
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

def convert_binary(image):
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(grey, 1, 255, cv2.THRESH_BINARY)
    return binary

def get_target(screenshot):

    # This should be managed through StateManager & InputManager:
    scope = Scope.x2

    # This should be managed through StateMAnager, InputManager, and ScreenShotManager
    raw = screenshot.image

    # Filter the image with the right mask:
    relevant_mask = ReferenceManager.get_mask(scope)
    raw = cv2.bitwise_and(raw, raw, mask=relevant_mask)

    # Convert to HSV:
    hsv = cv2.cvtColor(raw, cv2.COLOR_BGR2HSV)

    # Build a mask based on HSV filtering:
    mask = cv2.inRange(hsv, ReferenceManager.get_hsv(scope).lower, ReferenceManager.get_hsv(scope).upper)
    final_mask = cv2.erode(mask, np.ones((1, 2), np.uint8), iterations=1)
    final_mask = cv2.dilate(final_mask, np.ones((2, 3), np.uint8), iterations=4)

    # Apply the mask:
    hsv = cv2.bitwise_and(hsv, hsv, mask=final_mask)

    # Convert to binary:
    binary = convert_binary(hsv)

    # Identify components:
    components = cv2.connectedComponentsWithStats(binary, 4, cv2.CV_32S)
    labels = components[1] + 1
    labels = cv2.bitwise_and(labels, labels, mask=final_mask)
    stats = components[2]

    # find the biggest non-background shape label:
    counts = np.unique(labels, return_counts=True)
    invalid_label_indices = []
    for i, label in enumerate(list(counts[0].tolist())):
        if label == 0:
            invalid_label_indices.append(i)
    stats = [i for j, i in enumerate(stats) if j not in invalid_label_indices]

    if len(stats) <= 0:
        return Target(-1)
    else:
        biggest_shape = np.argmax(list(map(lambda s: s[4], stats)))

        # find the bounding box of the biggest non-background shape:
        target_x = stats[biggest_shape][cv2.CC_STAT_LEFT]
        target_y = stats[biggest_shape][cv2.CC_STAT_TOP]
        target_w = stats[biggest_shape][cv2.CC_STAT_WIDTH]
        target_h = stats[biggest_shape][cv2.CC_STAT_HEIGHT]

        # estimate the head from the bounding box:
        head_x = int(round(target_x + (target_w / 2.)))
        head_y = int(round(target_y + (target_h / 5.)))

        # walk the head around until you find a shot:
        aim_x = head_x
        aim_y = head_y
        step_size = 1
        step_direction = 1
        while True:
            if aim_x >= mask.shape[1] or aim_x < 0:
                aim_x = head_x
                step_size = 1
                aim_y += 4  # TODO be a little smarter about this
            if aim_y >= mask.shape[0]:
                raise Exception("Image Corruption")
            if mask[aim_y][aim_x] != 0:
                break
            else:
                aim_x += step_size * step_direction
                step_direction = -step_direction
                step_size += 1

        # try to center the shot on the shape:
        head_left = aim_x
        head_right = aim_x
        while head_left > 0 and final_mask[aim_y][head_left] != 0:
            head_left -= 1
        while head_right < (final_mask.shape[1] - 1) and final_mask[aim_y][head_right] != 0:
            head_right += 1
        aim_x = int(round(((head_left + head_right) / 2)))

        # TODO aim:
        print(aim_x, aim_y)

        c = cv2.Canny(raw, 100, 200)
        cv2.imshow('edges', c)
        # return # TODO remove debug

        # DEBUG:
        tgt = raw
        for i in [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)]:
            tgt[aim_y + i[0], head_left + i[1]] = [0, 255, 0]
        for i in [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)]:
            tgt[aim_y + i[0], head_right + i[1]] = [0, 255, 0]
        for i in [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)]:
            tgt[aim_y + i[0], aim_x + i[1]] = [255, 0, 0]

        # show the result:
        cv2.imshow('filter', binary)
        cv2.imshow('target', tgt)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return Target(1., aim_x, aim_y)

# TODO implement confidence
# TODO differential analysis (may require better detection)
# TODO evaluate edge detection
def main():

    # start the screenshotting thread:
    screenshotThread = BackgroundManager(float(1. / 1000), ScreenshotManager.get_screenshot, [Scope.x2])
    screenshotThread.start()

    # start the hook thread::
    # threading.Thread(target=InputManager.listen).start()
    # TODO the hook thread should trigger get_target on click, then trigger a Robot action

    # Invoke this for debug purposes
    get_target(Screenshot(get_image(), time.time()))

    print("Running...")

if __name__ == "__main__":
    main()
