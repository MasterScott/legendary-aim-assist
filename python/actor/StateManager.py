import time
import pynput
import numpy as np

# Used to track program state
aiming = False
shooting = False
shot = False
_beast_time = -1

# Used to store screenshots:
current_view = None
previous_view = None

# User settings:
shoot_button = pynput.mouse.Button.middle
shoot_key = pynput.keyboard.Key.delete
x_sensitivity = 12.5
y_sensitivity = 26
spray_mode = False
beast_key = "'z'"
scope = None

# Scope settings:
scope_key = pynput.keyboard.Key.alt
scoping = False
x1t_key = "'h'"
x1h_key = "'j"
x2_key = "'k"
x4v_key = "'l'"

# Debug
debug = True
screenshot_path = "out/"

# Helper functions:
def toggle_beast():
    global _beast_time
    if not beast_mode():
        _beast_time = time.time()
    else:
        _beast_time = -1
    print("Beast Mode = " + str(beast_mode()))


def beast_mode():
    return time.time() - _beast_time <= 45

def clear_view():
    global current_view, previous_view
    current_view = None
    previous_view = None

def update_view(view):
    global current_view, previous_view
    previous_view = current_view
    current_view = view

