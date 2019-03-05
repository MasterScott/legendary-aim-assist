import pynput
import time

from actor import StateManager

beast_time = -1

def listen():
    def on_click(x, y, button, pressed):
        if button == pynput.mouse.Button.right:
            StateManager.aiming = pressed
        return True

    def on_press(key):
        if str(key) == "'z'":
            StateManager.beast_mode = (not StateManager.beast_mode)
            print("Beast Mode = " + str(StateManager.beast_mode))
            beast_time = time.time()

    with pynput.keyboard.Listener(on_press=on_press) as kb_listener:
        with pynput.mouse.Listener(on_click=on_click) as mouse_listener:
            kb_listener.join()
            mouse_listener.join()
