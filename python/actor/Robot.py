from actor import StateManager
from actor import ReferenceManager
import pynput
import time
import numpy as np


# Smooths out a relative move (x, y) into multiple moves that still sum to x, y
def _smooth_moves(x, y, segments=3):
    x_moves = []
    for i in range(segments - 1):
        x_moves.append(np.random.uniform(1., (x - np.sum(x_moves))))
    x_moves.append(x - np.sum(x_moves))

    y_moves = []
    for i in range(segments - 1):
        y_moves.append(np.random.uniform(1., (y - np.sum(y_moves))))
        y_moves.append(y - np.sum(y_moves))
    return zip(x_moves, y_moves)


# TODO figure out how to normalize this based on mouse sensitivity (this is windows only)
def click(x, y):

    # adjust for aim point
    x -= ReferenceManager.get_aim(StateManager.scope)[0]
    y -= ReferenceManager.get_aim(StateManager.scope)[1]

    # Move the mouse:
    mouse = pynput.mouse.Controller()
    for move in _smooth_moves(x, y, 3):
        mouse.move(move[0], move[1])
        time.sleep(np.random.uniform(.001, .005))

    # Press the shoot button:
    keyboard = pynput.keyboard.Controller()
    keyboard.press(StateManager.shoot_key)
    time.sleep(.005)
    keyboard.release(StateManager.shoot_key)


