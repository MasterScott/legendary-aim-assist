import cv2
import numpy as np
import time
import threading
import math

from ReferenceManager import Scope
from BackgroundManager import BackgroundManager
import ScreenshotManager
import ReferenceManager
import InputManager


def distance(a, b):
    return math.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))

examples = {
    'out/1551643714397.png': (0, 0),
    'out/1551643715076.png': (0, 0),
    'out/1551643723461.png': (0, 0),
    'out/1551644022774.png': (0, 0),
    'out/1551644025498.png': (0, 0),
    'out/1551644032348.png': (0, 0),
    'out/1551644036303.png': (0, 0),
    'out/1551644037278.png': (136, 37),
}

# read in the image:
# raw = cv2.imread('out/1551643714397.png')  # clean sample
# raw = cv2.imread('out/1551643715076.png')  # occluded sample
# raw = cv2.imread('out/1551643723461.png')  # very close
# raw = cv2.imread('out/1551644022774.png')  # moderately far
# raw = cv2.imread('out/1551644025498.png') # noisy
# raw = cv2.imread('out/1551644032348.png')  # noisy
raw = cv2.imread('out/1551644036303.png')  # noisy
# raw = cv2.imread('out/1551644037278.png')  # hit marker
start = time.time()

# TODO expand AOI & add masks
# TODO differential analysis

# crop to AOI:

# HSV filter:
hsv = cv2.cvtColor(raw, cv2.COLOR_BGR2HSV)
original_mask = cv2.inRange(hsv, ReferenceManager.get_hsv(Scope.x2).lower, ReferenceManager.get_hsv(Scope.x2).upper)
# erode_mask = cv2.erode(original_mask, np.ones((2, 2), np.uint8), iterations=1)
final_mask = cv2.dilate(original_mask, np.ones((3, 2), np.uint8), iterations=3)
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
        aim_y += 4 # TODO be a little smarter about this
    if aim_y >= original_mask.shape[0]:
        raise Exception("Image Corruption")
    if original_mask[aim_y][aim_x] != 0:
        break
    else:
        aim_x += step_size * step_direction
        step_direction = -step_direction
        step_size += 1

# move the target farther in:
other_side = aim_x
while final_mask[aim_y][other_side] != 0:
    other_side -= step_direction

end = time.time()
print((end - start) * 1000)

print(aim_x, aim_y)
# TODO aim

# show the result:
cv2.imshow('test', raw)
cv2.imshow('bin', binary)
cv2.waitKey(0)
cv2.destroyAllWindows()

# start the screenshotting thread:
# screenshotThread = BackgroundManager(float(1./60), ScreenshotManager.screenshot, [Scope.x2])
# screenshotThread.start()

# start the hook thread::
# threading.Thread(target=InputManager.listen).start()

print("Running...")