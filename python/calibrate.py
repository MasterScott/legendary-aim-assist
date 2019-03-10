import time
import win32api, win32con


def main():

    # These should be configured in advance:
    fov = 110
    resolution = [1920, 1080]

    # This should be configured as you calibrate:
    sensitivity = [13, 23.5]  # 16.31, 29.37 (360), 12.5, 23 (test)
    mode = 'test'

    # Give you a second to alt + tab
    time.sleep(2.5)

    # Simulate the logic used in the real code:
    y_fov = (resolution[1] / resolution[0]) * fov
    if mode == 'test':
        x, y = 960 - 960, 484 - 540
    else:
        x, y = ((360. / fov) * resolution[0]), ((180. / y_fov) * resolution[1])

    x /= sensitivity[0]
    y /= sensitivity[1]

    # Adjust for windows API:
    x = int(round(x * 65535 / win32api.GetSystemMetrics(0)))
    y = int(round(y * 65535 / win32api.GetSystemMetrics(1)))

    def move(x, y):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y)

    # Spin one way or the other:
    if mode == 'x':
        print(x)
        for i in range(4):
            move(int(x / 4), 0)
            time.sleep(.5)
    elif mode == 'y':
        print(y)
        for i in range(4):
            move(0, int(y / 4))
            time.sleep(.5)
    elif mode == 'test':
        move(x, y)

if __name__ == "__main__":
    main()