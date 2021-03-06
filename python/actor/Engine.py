import cv2
import numpy as np
import time

from actor.ReferenceManager import Scope
from adt.Target import Target
from actor import ReferenceManager, ScreenshotManager, StateManager

def _convert_binary(image):
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(grey, 1, 255, cv2.THRESH_BINARY)
    return binary

def get_target(screenshot):

    scope = StateManager.scope
    raw = screenshot.image

    # Filter the image with the right mask:
    relevant_mask = ReferenceManager.get_mask(scope)
    raw = cv2.bitwise_and(raw, raw, mask=relevant_mask)

    # Convert to HSV:
    # print(screenshot)
    hsv = cv2.cvtColor(raw, cv2.COLOR_BGR2HSV)

    # Build a mask based on HSV filtering:
    mask = cv2.inRange(hsv, ReferenceManager.get_hsv(scope).lower, ReferenceManager.get_hsv(scope).upper)
    final_mask = cv2.erode(mask, np.ones((1, 2), np.uint8), iterations=1)
    final_mask = cv2.dilate(final_mask, np.ones((2, 3), np.uint8), iterations=4)

    # Apply the mask:
    hsv = cv2.bitwise_and(hsv, hsv, mask=final_mask)

    # Convert to binary:
    # binary = _convert_binary(hsv)

    # Use canny to convert to binary:
    c = cv2.Canny(hsv, 100, 200)
    small_mask = cv2.erode(mask, np.ones((2, 1), np.uint8), iterations=1)
    small_mask = cv2.erode(small_mask, np.ones((1, 2), np.uint8), iterations=1)
    small_c = cv2.bitwise_and(c, c, mask=small_mask)
    binary = cv2.dilate(small_c, np.ones((7, 7), np.uint8), iterations=2)

    # Fill holes:
    # im_floodfill = binary.copy()
    # h, w = im_floodfill.shape[:2]
    # flood_mask = np.zeros((h + 2, w + 2), np.uint8)
    # cv2.floodFill(im_floodfill, flood_mask, (0, 0), 255);
    # im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    # binary = binary | im_floodfill_inv

    # Identify components:
    components = cv2.connectedComponentsWithStats(binary, 4, cv2.CV_32S)
    labels = components[1] + 1
    labels = cv2.bitwise_and(labels, labels, mask=final_mask)
    stats = components[2]
    centroids = components[3]

    # find the biggest non-background shape label:
    counts = np.unique(labels, return_counts=True)
    invalid_label_indices = []
    for i, label in enumerate(list(counts[0].tolist())):
        if label == 0:
            invalid_label_indices.append(i)
    stats = [i for j, i in enumerate(stats) if j not in invalid_label_indices]
    centroids = [i for j, i in enumerate(centroids) if j not in invalid_label_indices]

    if len(stats) <= 0:
        print("No valid target found!")
        cv2.imwrite('out/fail-' + str(int(round(time.time() * 1000))) + '.png', raw)
        return Target(-1)
    else:
        biggest_shape = np.argmax(list(map(lambda s: s[4], stats)))

        # find the bounding box of the biggest non-background shape:
        target_x = stats[biggest_shape][cv2.CC_STAT_LEFT]
        target_y = stats[biggest_shape][cv2.CC_STAT_TOP]
        target_w = stats[biggest_shape][cv2.CC_STAT_WIDTH]
        target_h = stats[biggest_shape][cv2.CC_STAT_HEIGHT]

        # estimate the head from the bounding box:
        head_x = int(round((stats[biggest_shape][0] + int(round(target_x + (target_w / 2.)))) / 2.))
        head_y = int(round(target_y + (target_h / 4.)))

        # walk the head around until you find a shot:
        aim_x = head_x
        aim_y = head_y
        left = aim_x
        right = aim_x
        while left > 0 or right < binary.shape[1]:
            if left > 0 and binary[aim_y][left] != 0:
                aim_x = left
                break
            elif right < binary.shape[1] and binary[aim_y][right] != 0:
                aim_x = right
                break
            else:
                left -= 1
                right += 1

        # try to center the shot on the shape:
        head_left = aim_x
        head_right = aim_x
        while head_left > 0 and binary[aim_y][head_left] != 0:
            head_left -= 1
        while head_right < (binary.shape[1] - 1) and binary[aim_y][head_right] != 0:
            head_right += 1
        aim_x = int(round(((head_left + head_right) / 2)))

        # show the result:
        if StateManager.debug:

            tgt = raw
            for i in [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)]:
                tgt[aim_y + i[0], head_left + i[1]] = [0, 255, 0]
            for i in [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)]:
                tgt[aim_y + i[0], head_right + i[1]] = [0, 255, 0]
            for i in [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)]:
                tgt[aim_y + i[0], aim_x + i[1]] = [255, 0, 0]

            cv2.imshow('post-canny filter', binary)
            cv2.imshow('lines', c)
            cv2.imshow('hsv', hsv)
            cv2.imshow('target', tgt)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return Target(1., aim_x, aim_y, centroids[biggest_shape])
