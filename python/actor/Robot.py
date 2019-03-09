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
        x_moves.append(np.random.randint(1., (x - np.sum(x_moves))) + np.random.randint(-int(x/10), int(x/10)))
    x_moves.append(x - np.sum(x_moves))

    y_moves = []
    for i in range(segments - 1):
        y_moves.append(np.random.randint(1, (y - np.sum(y_moves))) + np.random.randint(-int(y/10), int(y/10)))
    y_moves.append(y - np.sum(y_moves))

    return zip(x_moves, y_moves)


def move(x, y):

    # Adjust for aim point
    x -= ReferenceManager.get_aim(StateManager.scope)[0]
    y -= ReferenceManager.get_aim(StateManager.scope)[1]

    # Adjust for sensitivity
    x /= StateManager.x_sensitivity
    y /= StateManager.y_sensitivity

    # Adjust for windows API:
    x = int(round(x * 65535 / win32api.GetSystemMetrics(0)))
    y = int(round(y * 65535 / win32api.GetSystemMetrics(1)))

    # Move the mouse:
    for smooth_move in _smooth_moves(x, y, 3):
        # print(x, smooth_move, smooth_move[0])
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, smooth_move[0], smooth_move[1])
        # time.sleep(np.random.uniform(.001, .003))


def shoot():
    x, y = win32api.GetCursorPos()
    if StateManager.shooting:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        # print(time.time() - StateManager.start_time)  # TODO remove debug
        time.sleep(np.random.uniform(.001, .003))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)




def act():
    if StateManager.aiming and StateManager.shooting:
        if StateManager.spray_mode or not StateManager.shot:
            if StateManager.beast_mode() or (StateManager.scope in [ReferenceManager.Scope.x1t]):

                # Sleep until we have a current view
                while not StateManager.current_view:
                    time.sleep(.0001)

                # Analyze the current view
                past_time = StateManager.current_view.timestamp
                past_target = Engine.get_target(StateManager.current_view)

                # Sleep until a new view comes in (we've been treating the old current view as the past view)
                while StateManager.current_view.timestamp <= past_time:
                    time.sleep(.0001)
                current_time = StateManager.current_view.timestamp
                current_target = Engine.get_target(StateManager.current_view)

                # If we're confident in both views, extrapolate the future state based on the target delta
                x, y = current_target.x, current_target.y
                if current_target.confidence > .5:
                    if past_target.confidence > .5:
                        x_delta = current_target.centroid[0] - past_target.centroid[0]
                        y_delta = current_target.centroid[1] - past_target.centroid[1]
                        now = time.time() * 1000
                        time_ratio = max(1., ((now - current_time) / (current_time - past_time))) * .5
                        x_delta_pred, y_delta_pred = x_delta * time_ratio, y_delta * time_ratio
                        x, y = x + x_delta_pred, y + y_delta_pred
                    move(x, y)
                    shoot()
                StateManager.shot = True
