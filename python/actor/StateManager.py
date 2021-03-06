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
shoot_key = 0x2E
x_sensitivity = 13
y_sensitivity = 23.5
spray_mode = False
beast_key = "'z'"
scope = None

# Scope settings:
scope_key = pynput.keyboard.Key.ctrl_l
scoping = False
x1o_key = "'h'"
x1h_key = "'j'"
x1t_key = "'k'"
x2_key = "'l'"
x4v_key = "';'"

# Debug
debug = False
screenshot_path = "out/"
start_time = -1

# Helper functions:
def toggle_beast():
    global _beast_time
    if not beast_mode():
        _beast_time = time.time()
    else:
        _beast_time = -1
    #print("Beast Mode = " + str(beast_mode()))


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

