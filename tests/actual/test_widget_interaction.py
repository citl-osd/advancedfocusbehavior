import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import pytest

from math import isclose

from common import run_in_app
from kivy_garden.advancedfocusbehavior import FocusBoxLayout, FocusButton, \
            FocusCarousel, FocusTextInput, FocusWidget, FocusCheckBox, \
            FocusSlider, FocusToggleButton, FocusScreen, FocusScreenManager, \
            FocusVideoPlayer


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


@run_in_app(app_class=CheckActionApp, timeout=20)
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


@run_in_app(app_class=CheckActionApp)
def test_checkbox():
    app = App.get_running_app()
    container = FocusBoxLayout(orientation='vertical', padding=10, spacing=10)
    lb = Label(text='Activate the checkbox, then press the button below it.')
    cb = FocusCheckBox()
    btn = FocusButton(text='Test checkbox')

    def press_me(*args):
        assert cb.active
        app.did_action = True
        app.stop()

    btn.bind(on_press=press_me)

    for widg in (lb, cb, btn):
        container.add_widget(widg)

    app.root.add_widget(container)
    return True


@run_in_app(app_class=CheckActionApp)
def test_toggle_button():
    app = App.get_running_app()
    container = FocusBoxLayout(orientation='vertical', padding=10, spacing=10)
    lb = Label(text='Activate the toggle button, then press the button below it.')
    tb = FocusToggleButton(text='off')
    btn = FocusButton(text='Test toggle button')

    def update_toggle_label(tbtn, val):
        tbtn.text = 'on' if val == 'down' else 'off'


    def press_me(*args):
        assert tb.state == 'down'
        app.did_action = True
        app.stop()

    tb.bind(state=update_toggle_label)
    btn.bind(on_press=press_me)

    for widg in (lb, tb, btn):
        container.add_widget(widg)

    app.root.add_widget(container)
    return True


@run_in_app(app_class=CheckActionApp)
def test_slider():
    value = 48
    app = App.get_running_app()
    container = FocusBoxLayout(orientation='vertical', padding=10, spacing=10)
    instruction_label = Label(text=f'Set the slider to {value}')
    pos_label = Label()
    slider = FocusSlider()
    btn = FocusButton(text='Submit')

    def update_pos_label(slider, value):
        pos_label.text = str(int(value))


    def press_me(*args):
        assert int(slider.value) == value
        app.did_action = True
        app.stop()


    slider.bind(value=update_pos_label)
    btn.bind(on_press=press_me)

    for widg in (instruction_label, pos_label, slider, btn):
        container.add_widget(widg)

    app.root.add_widget(container)
    return True


@run_in_app(app_class=CheckActionApp)
def test_screen_manager():
    app = App.get_running_app()
    app.step_1 = False

    instructions = Label(text=('Press the button on the next screen, then press'
                                ' the button at the bottom of the app.'))

    s1 = FocusScreen(name='screen_1')
    container_1 = FocusBoxLayout(orientation='vertical', padding=30, spacing=30)
    to_screen_2 = FocusButton(text='To screen 2 ->')
    container_1.add_widget(to_screen_2)
    s1.add_widget(container_1)

    s2 = FocusScreen(name='screen_2')
    container_2 = FocusBoxLayout(orientation='vertical', padding=30, spacing=30)
    step_1_btn = FocusButton(text='Press me first!')
    container_2.add_widget(step_1_btn)
    s2.add_widget(container_2)

    submit_btn = FocusButton(text='Submit')
    manager = FocusScreenManager()

    def press_step_1(*args):
        app.step_1 = True


    def press_to_screen_2(*args):
        manager.current = 'screen_2'


    def submit(*args):
        if app.step_1:
            app.did_action = True
            app.stop()


    to_screen_2.bind(on_press=press_to_screen_2)
    step_1_btn.bind(on_press=press_step_1)
    submit_btn.bind(on_press=submit)

    manager.add_widget(s1)
    manager.add_widget(s2)

    app.root.add_widget(instructions)
    app.root.add_widget(manager)
    app.root.add_widget(submit_btn)

    return True


@run_in_app(app_class=CheckActionApp, timeout=60)
def test_video_player():
    target = 5  # seconds
    app = App.get_running_app()
    container = FocusBoxLayout(orientation='vertical', padding=30, spacing=30)
    instructions = Label(text=(f'1. Navigate to {target} seconds in the video\n'
                                '2. Mute the audio'), size_hint_y=0.1)
    player = FocusVideoPlayer(source='tests/actual/test_data/mandelbrot.mp4')
    submit = FocusButton(text='Submit', size_hint_y=0.1)

    def on_submit(*args):
        assert isclose(target, player.position, abs_tol=1)
        assert player.volume == 0
        app.did_action = True
        app.stop()

    submit.bind(on_press=on_submit)
    container.add_widget(instructions)
    container.add_widget(player)
    container.add_widget(submit)

    app.root.add_widget(container)

    return True
