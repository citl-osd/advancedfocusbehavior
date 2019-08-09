import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
import pytest

from common import run_in_app, test_window_name
from kivy_garden.advancedfocusbehavior import FocusButton, FocusCarousel, FocusTextInput, FocusWidget


@run_in_app
def test_get_focus_upon_entering():
    # If there are no focused widgets, the first focusable widget should receive focus
    container = BoxLayout()
    widg = FocusWidget()
    assert not widg.focus
    app = App.get_running_app()
    container.add_widget(widg)
    app.root.add_widget(container)
    assert widg.focus


@run_in_app
def test_pyautogui_interaction():
    container = BoxLayout()
    text = FocusTextInput(multiline=False, write_tab=False)
    container.add_widget(text)

    app = App.get_running_app()
    app.root.add_widget(container)

    def check_keys(req, result):
        try:
            assert text.text == 'some_keys'

        finally:
            app.stop()

    Clock.schedule_once(lambda _: UrlRequest('http://localhost:8090/type?keys=some_keys', check_keys), 1)
    return True


@run_in_app
def test_cycle_through_focusables():
    container = BoxLayout()
    focus_widgets = [FocusWidget() for _ in range(3)]

    for widg in focus_widgets:
        container.add_widget(widg)

    focus_1, focus_2, focus_3 = focus_widgets
    app = App.get_running_app()
    app.root.add_widget(container)

    def cycle_prev(req, result):
        try:
            assert focus_1.focus
            assert not focus_2.focus
            assert not focus_3.focus

        finally:
            app.stop()


    def cycle_next(req, result):
        try:
            assert not focus_1.focus
            assert focus_2.focus
            assert not focus_3.focus

            Clock.schedule_once(lambda _: UrlRequest('http://localhost:8090/hotkey?keys=["shift", "tab"]', cycle_prev), 1)

        except AssertionError:
            app.stop()

    assert focus_1.focus
    assert not focus_2.focus
    assert not focus_3.focus

    Clock.schedule_once(lambda _: UrlRequest('http://localhost:8090/press?key=tab', cycle_next), 1)
    return True


# TODO: move to different file
@run_in_app
def test_focus_buttons():
    app = App.get_running_app()
    self = test_focus_buttons
    self.got_pushed = False

    def push_me(*args):
        print('pushed called')
        self.got_pushed = True

    def push_test(req, result):
        try:
            assert self.got_pushed

        finally:
            app.stop()


    container = BoxLayout()
    btn = FocusButton(on_press=push_me)
    container.add_widget(btn)
    app.root.add_widget(container)
    assert btn.focus

    Clock.schedule_once(lambda _: UrlRequest('http://localhost:8090/press?key=enter', push_test), 5)
    return True
