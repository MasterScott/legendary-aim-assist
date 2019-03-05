import time
import threading
from threading import Thread
from threading import Event

class BackgroundManager(Thread):
    def __init__(self, interval_seconds, callback, args):
        super().__init__()
        self.stop_event = Event()
        self.interval_seconds = interval_seconds
        self.callback = callback
        self.args = args

    def run(self):
        while not self.stop_event.wait(self.interval_seconds):
            self.callback(*self.args)

    def stop(self):
        self.stop_event.set()
