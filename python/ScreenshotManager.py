import mss, mss.tools
from PIL import Image
import time

import ReferenceManager
import StateManager


def screenshot(scope, save=True):
    if True:
    # if StateManager.aiming and StateManager.beast_mode:
        snapshot = _gsk_screenshot(ReferenceManager.get_aoi(scope))
        if save:
            save_path = "out_test/" + str(int(round(time.time() * 1000))) + ".png"
            snapshot.save(save_path)

def _gsk_screenshot(aoi):
    monitor = {"top": aoi.y, "left": aoi.x, "width": aoi.w, "height": aoi.h}
    with mss.mss() as sct:
        sct_img = sct.grab(monitor)
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
