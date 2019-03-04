import cv2
import numpy as np
import time
import threading
import math
import sys

from ReferenceManager import Scope
from BackgroundManager import BackgroundManager
import ScreenshotManager
import ReferenceManager
import InputManager


def distance(a, b):
    return math.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))

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

# used to create masks:
# test = cv2.imread('out/1551643712955.png')
# hsv = cv2.cvtColor(test, cv2.COLOR_BGR2HSV)
# test_mask = cv2.inRange(hsv, np.array([0, 115, 0]), np.array([1, 255, 255]))
# hsv = cv2.bitwise_and(hsv, hsv, mask=test_mask)
# grey = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
# _, mask = cv2.threshold(grey, 1, 255, cv2.THRESH_BINARY)
# mask = cv2.bitwise_not(mask)
# cv2.imwrite('data/masks/x2/mask.png', mask)
# cv2.imshow('t', mask)


# read in the image:
# raw = cv2.imread('out/1551643714397.png')  # clean sample
# raw = cv2.imread('out/1551643715076.png')  # occluded sample
# raw = cv2.imread('out/1551643723461.png')  # very close
# raw = cv2.imread('out/1551644022774.png')  # moderately far
# raw = cv2.imread('out/1551644025498.png') # noisy
# raw = cv2.imread('out/1551644032348.png')  # noisy
raw = cv2.imread('out/1551644036303.png')  # noisy (failing)
# raw = cv2.imread('out/1551644037278.png')  # hit marker
start = time.time()

relevant_mask = ReferenceManager.get_mask(Scope.x2)
big_mask = cv2.dilate(relevant_mask, np.ones((2, 2), np.uint8), iterations=1)
raw = cv2.bitwise_and(raw, raw, mask=big_mask)
# TODO differential analysis

# crop to AOI:

# HSV filter:
hsv = cv2.cvtColor(raw, cv2.COLOR_BGR2HSV)
original_mask = cv2.inRange(hsv, ReferenceManager.get_hsv(Scope.x2).lower, ReferenceManager.get_hsv(Scope.x2).upper)
erode_mask = cv2.erode(original_mask, np.ones((1, 2), np.uint8), iterations=1)
final_mask = cv2.dilate(erode_mask, np.ones((2, 3), np.uint8), iterations=4)
hsv = cv2.bitwise_and(hsv, hsv, mask=final_mask)

# convert to binary:
grey = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(grey, 1, 255, cv2.THRESH_BINARY)

# identify objects:
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
    if aim_x >= original_mask.shape[1] or aim_x < 0:
        aim_x = head_x
        step_size = 1
        aim_y += 4  # TODO be a little smarter about this
    if aim_y >= original_mask.shape[0]:
        raise Exception("Image Corruption")
    if original_mask[aim_y][aim_x] != 0:
        break
    else:
        aim_x += step_size * step_direction
        step_direction = -step_direction
        step_size += 1

head_left = aim_x
head_right = aim_x
while head_left > 0 and final_mask[aim_y][head_left] != 0:
    head_left -= 1
while head_right < (final_mask.shape[1] - 1) and final_mask[aim_y][head_right] != 0:
    head_right += 1

aim_x = int(round(((head_left + head_right) / 2)))

end = time.time()
print((end - start) * 1000)

print(aim_x, aim_y)
# TODO aim

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

# start the screenshotting thread:
# screenshotThread = BackgroundManager(float(1./1000), ScreenshotManager.screenshot, [Scope.x2])
# screenshotThread.start()

# start the hook thread::
# threading.Thread(target=InputManager.listen).start()

print("Running...")