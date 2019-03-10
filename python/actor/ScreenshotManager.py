import mss, mss.tools
from PIL import Image
import time

from actor import StateManager, ReferenceManager
from adt.Screenshot import Screenshot
import numpy as np
import cv2

# Updates the statemanager view, and optionally saves it as an image
# Typically takes <10 ms, or <30ms if saving.
def update_view(save=False):
    if StateManager.aiming and StateManager.beast_mode():
        timestamp = int(round(time.time() * 1000))
        image = _gsk_screenshot(ReferenceManager.get_aoi(StateManager.scope))
        screenshot = Screenshot(image, timestamp)
        # screenshot = Screenshot(cv2.imread('data/samples/x1h/1552066529854.png'), timestamp)
        # cv2.imshow('t', screenshot.image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        if save:
            cv2.imwrite(StateManager.screenshot_path + str(timestamp) + ".png", screenshot.image)
        StateManager.update_view(screenshot)

# Private method used to efficiently take screenshots
def _gsk_screenshot(aoi):
    monitor = {"top": aoi.y, "left": aoi.x, "width": aoi.w, "height": aoi.h}
    with mss.mss() as sct:
        sct_img = sct.grab(monitor)
        return np.array(sct_img)
