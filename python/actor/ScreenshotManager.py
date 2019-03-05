import mss, mss.tools
from PIL import Image
import time

from actor import StateManager, ReferenceManager
from adt.Screenshot import Screenshot

# Returns a screenshot and optionally saves it
# Typically takes <10 ms, or <30ms if saving.
def get_screenshot(scope, save=True):
    if StateManager.aiming and StateManager.beast_mode:
        image = _gsk_screenshot(ReferenceManager.get_aoi(scope))
        timestamp = int(round(time.time() * 1000))
        screenshot = Screenshot(image, timestamp)
        if save:
            image.save("out_test/" + str(timestamp) + ".png")
        return screenshot

# Private method used to efficiently take screenshots
def _gsk_screenshot(aoi):
    monitor = {"top": aoi.y, "left": aoi.x, "width": aoi.w, "height": aoi.h}
    with mss.mss() as sct:
        sct_img = sct.grab(monitor)
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
