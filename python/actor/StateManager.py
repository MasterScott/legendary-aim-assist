from actor.ReferenceManager import Scope
import time
import pynput

aiming = False
scope = Scope.x2
_beast_time = -1
shoot_button = pynput.mouse.Button.middle
shoot_key = pynput.keyboard.Key.delete
debug = True

def toggle_beast():
    global _beast_time
    if not beast_mode():
        _beast_time = time.time()
    else:
        _beast_time = -1


def beast_mode():
    return time.time() - _beast_time <= 45
