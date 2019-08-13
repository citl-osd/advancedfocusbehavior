import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

import pytest

from functools import wraps
from pathlib import Path
import sys

focus_dest = str(Path(__file__).parents[2].resolve())
if focus_dest not in sys.path:
    sys.path.append(focus_dest)

def run_in_app(app_class=App, timeout=15):

    @wraps(run_in_app)
    def real_run_in_app(func):

        @wraps(func)
        def wrapper():

            def func_as_callback(dt):

                # Tests that need to do async things (like keypresses) must close themselves
                keep_app_alive = False
                try:
                    keep_app_alive = func()

                finally:
                    if not keep_app_alive:
                        App.get_running_app().stop()


            Clock.schedule_once(func_as_callback, 2)
            Clock.schedule_once(lambda _: pytest.fail('No user interaction given.'), timeout)
            app = app_class()
            app.title = func.__name__
            app.root = BoxLayout(padding=10, spacing=10)
            app.run()

        return wrapper

    return real_run_in_app
