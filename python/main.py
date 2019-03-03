import cv2
import numpy as np
import time
import threading

from ReferenceManager import Scope
from BackgroundManager import BackgroundManager
import ScreenshotManager
import ReferenceManager
import InputManager

# read in the image:
img = cv2.imread('../examples/beast-mode/x2/0.png')

# transform the image:

# crop to AOI:
aoi = ReferenceManager.get_aoi(Scope.x2)
img = img[aoi.y:aoi.y+aoi.h, aoi.x:aoi.x+aoi.w]

# filter for color:
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(img, ReferenceManager.get_hsv(Scope.x2).lower, ReferenceManager.get_hsv(Scope.x2).upper)
img = cv2.bitwise_and(img, img, mask=mask)

# erode and dilate:
img = cv2.erode(img, np.ones((2, 1), np.uint8), iterations=1)
img = cv2.dilate(img, np.ones((2, 2), np.uint8), iterations=5)

# identify objects:
img[img != 0] = 255
# cv2.floodFill(img, None, (0, 0), 255)
# _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
# img = cv2.bitwise_not(img)
# h, w = img.shape[:2]
# mask = np.zeros((h + 2, w + 2), np.uint8)
# cv2.floodFill(img, mask, (0, 0), 255)


# show the result:
# cv2.imshow('test', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# start the screenshotting thread:
screenshotThread = BackgroundManager(float(1./60), ScreenshotManager.screenshot, [Scope.x2])
screenshotThread.start()

# start the hook thread::
threading.Thread(target=InputManager.listen).start()

print("Running...")