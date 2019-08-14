import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import pytest

from common import run_in_app
from kivy_garden.advancedfocusbehavior import FocusBoxLayout, FocusButton, \
            FocusCarousel, FocusTextInput, FocusWidget


class CheckActionApp(App):
    """"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.did_action = False


    def stop(self):
        super().stop()
        assert self.did_action


# TODO: move to different file
@run_in_app(app_class=CheckActionApp)
def test_focus_buttons():
    app = App.get_running_app()
    self = test_focus_buttons

    def push_me(*args):
        app.did_action = True
        app.stop()


    container = FocusBoxLayout()
    btn = FocusButton(text='Press Enter', on_press=push_me)
    container.add_widget(btn)
    app.root.add_widget(container)
    assert btn.focus

    return True


@run_in_app(app_class=CheckActionApp)
def test_cycle_through_focusables():
    app = App.get_running_app()
    app.step_1 = False

    def focus_1(btn, state):
        if not state:
            return

        if app.step_1:
            app.did_action = True
            app.stop()


    def focus_2(btn, state):
        if not state:
            return

        if app.step_1:
            app.stop()

        else:
            app.step_1 = True


    def focus_3(btn, state):
        if not state:
            return

        app.stop()


    container = FocusBoxLayout(orientation='vertical', padding=20, spacing=20)
    container.add_widget(Label(text=('Press Tab once to cycle to the next widget, '
                                     'then press Shift+Tab once to cycle back.')))
    first = FocusButton(text='button 1')
    second = FocusButton(text='button 2')
    third = FocusButton(text='button 3')

    first.bind(focus=focus_1)
    second.bind(focus=focus_2)
    third.bind(focus=focus_3)

    for btn in (first, second, third):
        container.add_widget(btn)

    app.root.add_widget(container)
    assert first.focus
    return True


@run_in_app(app_class=CheckActionApp, timeout=None)
def test_carousel():
    app = App.get_running_app()
    app.step_1 = False

    def press_1(*args):
        app.step_1 = True


    def press_2(*args):
        if app.step_1:
            app.did_action = True
            app.stop()


    car = FocusCarousel(direction='right')
    car.add_widget(Label(text='Navigate to the right in the carousel'))

    btn_1 = FocusButton(text='Press me')
    btn_2 = FocusButton(text='Press me after you\'ve pressed the other button')

    btn_1.bind(on_press=press_1)
    btn_2.bind(on_press=press_2)

    car.add_widget(btn_1)
    app.root.add_widget(car)
    app.root.add_widget(btn_2)

    return True
