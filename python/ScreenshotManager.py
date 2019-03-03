from PIL import ImageGrab
import time

import ReferenceManager
import StateManager


def screenshot(scope, save=True):
    if StateManager.aiming and StateManager.beast_mode:
        aoi = ReferenceManager.get_aoi(scope)
        snapshot = ImageGrab.grab(bbox=(aoi.x, aoi.y, aoi.x + aoi.w, aoi.y + aoi.h))
        if save:
            save_path = "out/" + str(int(round(time.time() * 1000))) + ".png"
            snapshot.save(save_path)
