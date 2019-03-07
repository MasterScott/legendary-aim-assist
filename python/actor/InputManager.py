import pynput
import time

from actor import StateManager
from actor import ScreenshotManager
from actor import ReferenceManager
from actor import Robot
from actor import Engine

from adt.Screenshot import Screenshot
from adt.Target import Target

beast_time = -1

def listen():
    def on_click(x, y, button, pressed):

        # When aiming is toggled, update aiming and potentially clear views:
        if button == pynput.mouse.Button.right:
            StateManager.aiming = pressed
            if not pressed:
                StateManager.clear_view()

        # When shooting or aiming is toggled, update shooting and potentially clear shot:
        if button == StateManager.shoot_button or button == pynput.mouse.Button.right:
            StateManager.shooting = pressed and StateManager.aiming
            if not pressed:
                StateManager.shot = False

        return True

    def on_press(key):
        if str(key) == StateManager.scope_key:
            StateManager.scoping = True
        elif str(key) == StateManager.beast_key:
            StateManager.toggle_beast()
        elif str(key) in ReferenceManager.key_dict():
            StateManager.scope = ReferenceManager.key_dict()[str(key)]

    def on_release(key):
        if str(key) == StateManager.scope_key:
            StateManager.scoping = False

    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as kb_listener:
        with pynput.mouse.Listener(on_click=on_click) as mouse_listener:
            kb_listener.join()
            mouse_listener.join()
