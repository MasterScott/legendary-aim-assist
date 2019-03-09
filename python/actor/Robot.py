from actor import StateManager
from actor import ReferenceManager
from actor import Engine
import pynput
import win32api, win32con
import time
import numpy as np
import time


# Smooths out a relative move (x, y) into multiple moves that still sum to x, y
def _smooth_moves(x, y, segments=3):
    x_moves = []
    for i in range(segments - 1):
        x_moves.append(np.random.uniform(1., (x - np.sum(x_moves))) + np.random.uniform(-(x/10.), (x/10.)))
    x_moves.append(x - np.sum(x_moves))

    y_moves = []
    for i in range(segments - 1):
        y_moves.append(np.random.uniform(1., (y - np.sum(y_moves))) + np.random.uniform(-(y / 10.), (y / 10.)))
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
    x, y = win32api.GetCursorPos()
    if StateManager.shooting:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        time.sleep(np.random.uniform(.004, .006))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)



def act():
    if StateManager.aiming and StateManager.shooting:
        if StateManager.spray_mode or not StateManager.shot:
            if StateManager.beast_mode() or (StateManager.scope in [ReferenceManager.Scope.x1t]):
                while not StateManager.current_view:
                    time.sleep(.001)
                target = Engine.get_target(StateManager.current_view)
                if target.confidence > .5:
                    move(target.x, target.y)
                    shoot()
                StateManager.shot = True
