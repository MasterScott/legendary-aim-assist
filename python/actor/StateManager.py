from actor.ReferenceManager import Scope, HsvBounds
import time
import pynput
import numpy as np

# Used to track program state
aiming = False
shooting = False
_beast_time = -1
scope = Scope.x2

# User settings:
shoot_button = pynput.mouse.Button.middle
shoot_key = pynput.keyboard.Key.delete
mouse_sensitivity = 1.  # TODO
spray_mode = False

# Debug
debug = False# Helper functions:
def toggle_beast():
    global _beast_time
    if not beast_mode():
        _beast_time = time.time()
    else:
        _beast_time = -1


def beast_mode():
    return time.time() - _beast_time <= 45
