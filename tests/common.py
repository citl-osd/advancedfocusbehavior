import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.clock import Clock
from pygetwindow import getWindowsWithTitle

from functools import wraps
from pathlib import Path
import sys

focus_dest = str(Path(__file__).parents[1].resolve())
if focus_dest not in sys.path:
    sys.path.append(focus_dest)

test_window_name = 'advancedfocusbehavior_test'

def run_in_app(func):

    @wraps(func)
    def wrapper():

        def func_as_callback(dt):
            try:
                #getWindowsWithTitle(test_window_name)[0].focus()
                func()

            finally:
                App.get_running_app().stop()

        Clock.schedule_once(func_as_callback, 1)
        app = App()
        app.title = test_window_name
        app.run()

    return wrapper
