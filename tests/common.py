import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.clock import Clock
from pygetwindow import getWindowsWithTitle

from functools import wraps


test_window_name = 'advancedfocusbehavior_test'


def focus_kivy_window():
    getWindowsWithTitle(test_window_name)[0].focus()


def run_in_app(func):

    @wraps(func)
    def wrapper():

        def func_as_callback(dt):
            try:
                focus_kivy_window()
                func()

            finally:
                App.get_running_app().stop()

        Clock.schedule_once(func_as_callback)
        app = App()
        app.title = test_window_name
        app.run()

    return wrapper
