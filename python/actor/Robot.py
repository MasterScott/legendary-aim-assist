from actor import StateManager
from actor import ReferenceManager
import pynput
import time

# Smooths out a relative move (x, y) into multiple moves that still end in x, y
def _smooth_moves(x, y, segments=2):
    return [(x, y)]

# TODO figure out how to normalize this based on mouse sensitivity (this is windows only)
def click(x, y):

    # adjust for AOI (todo is this absolute move?)
    # x += ReferenceManager.get_aoi(StateManager.Scope).x
    # y += ReferenceManager.get_aoi(StateManager.Scope).y


    mouse = pynput.mouse.Controller()
    print("Moving ", x, y)
    print(mouse.position)
    mouse.position = (x, y)  # TODO use smooth moves

    # Press the shoot button:
    keyboard = pynput.keyboard.Controller()
    keyboard.press(StateManager.shoot_key)
    time.sleep(.005)
    keyboard.release(StateManager.shoot_key)


