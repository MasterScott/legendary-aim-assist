from actor import StateManager
from actor import ReferenceManager
from actor import Engine
import pynput
import win32api, win32con
import time
import numpy as np


# Smooths out a relative move (x, y) into multiple moves that still sum to x, y
def _smooth_moves(x, y, segments=3):
    x_moves = []
    for i in range(segments - 1):
        x_moves.append(np.random.uniform(1., (x - np.sum(x_moves))) + np.random.randint(-5, 5))
    x_moves.append(x - np.sum(x_moves))

    y_moves = []
    for i in range(segments - 1):
        y_moves.append(np.random.uniform(1., (y - np.sum(y_moves))) + np.random.randint(-5, 5))
    y_moves.append(y - np.sum(y_moves))

    return zip(x_moves, y_moves)

def move(x, y):

    # Adjust for aim point
    x -= ReferenceManager.get_aim(StateManager.scope)[0]
    y -= ReferenceManager.get_aim(StateManager.scope)[1]

    # Adjust for sensitivity
    x /= StateManager.x_sensitivity
    y /= StateManager.y_sensitivity

    # Move the mouse:
    for move in _smooth_moves(x, y, 3):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,
                             int(move[0] * 65535 / win32api.GetSystemMetrics(0)), int(move[1] * 65535 / win32api.GetSystemMetrics(1)))
        time.sleep(np.random.uniform(.001, .005))


def shoot():
    keyboard = pynput.keyboard.Controller()
    if StateManager.shooting:
        keyboard.press(StateManager.shoot_key)
        time.sleep(np.random.uniform(.004, .006))
    if not StateManager.shooting:
        keyboard.release(StateManager.shoot_key)

