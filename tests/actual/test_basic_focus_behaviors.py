import pyautogui
pyautogui.PAUSE = 0.5
import pytest

import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from common import run_in_app
from kivy_garden.advancedfocusbehavior import FocusButton, FocusCarousel, FocusTextInput, FocusWidget


@run_in_app
def test_get_focus_upon_entering():
    # If there are no focused widgets, the first focusable widget should receive focus
    container = BoxLayout()
    widg = FocusWidget()
    app = App.get_running_app()
    container.add_widget(widg)
    app.root = container
    assert widg.focus


@run_in_app
def test_cycle_through_focusables():
    container = BoxLayout()
    focus_widgets = [FocusWidget() for _ in range(3)]

    for widg in focus_widgets:
        container.add_widget(widg)

    focus_1, focus_2, focus_3 = focus_widgets
    app = App.get_running_app()
    app.root = container

    assert focus_1.focus   # tested in test_get_focus_upon_entering
    pyautogui.press('tab')
    assert focus_2.focus

    pyautogui.hotkey('shift', 'tab')
    assert focus_1.focus


# TODO: move to different file
@run_in_app
def test_focus_buttons():
    self = test_focus_buttons
    self.got_pushed = False

    def push_me(*args):
        self.got_pushed = True

    app = App.get_running_app()
    app.root = FocusButton(on_press=push_me)

    pyautogui.press('enter')
    assert self.got_pushed
