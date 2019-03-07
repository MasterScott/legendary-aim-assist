import pynput
import time

from actor import StateManager
from actor import ScreenshotManager
from actor import Robot
from actor import Engine

from adt.Screenshot import Screenshot
from adt.Target import Target

beast_time = -1

def listen():
    def on_click(x, y, button, pressed):
        if button == pynput.mouse.Button.right:
            StateManager.aiming = pressed
        if button == StateManager.shoot_button:
            StateManager.shooting = pressed
            Engine.shoot()
        return True

    def on_press(key):
        if str(key) == "'z'":
            StateManager.toggle_beast()
            print("Beast Mode = " + str(StateManager.beast_mode()))

    with pynput.keyboard.Listener(on_press=on_press) as kb_listener:
        with pynput.mouse.Listener(on_click=on_click) as mouse_listener:
            kb_listener.join()
            mouse_listener.join()
