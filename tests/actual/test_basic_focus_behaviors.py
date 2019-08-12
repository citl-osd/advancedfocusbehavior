import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import pytest

from common import run_in_app
from kivy_garden.advancedfocusbehavior import FocusApp, FocusButton, FocusCarousel, FocusTextInput, FocusWidget


class CheckActionApp(FocusApp):
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


    container = BoxLayout()
    btn = FocusButton(text='Press Enter', on_press=push_me)
    container.add_widget(btn)
    app.root.add_widget(container)
    #assert btn.focus

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


    container = BoxLayout(orientation='vertical', padding=20, spacing=20)
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
    #assert first.focus
    return True
