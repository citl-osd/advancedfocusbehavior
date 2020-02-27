import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.treeview import TreeViewLabel
import pytest

from math import isclose

from common import run_in_app
from kivy_garden.advancedfocusbehavior import *


def default_container():
    return FocusBoxLayout(orientation='vertical', padding=30, spacing=30)


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


    container = default_container()
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

    container = default_container()
    btn_1 = FocusButton(text='Press me')
    btn_2 = FocusButton(text='Press me after you\'ve pressed the other button')

    btn_1.bind(on_press=press_1)
    btn_2.bind(on_press=press_2)

    container.add_widget(btn_1)
    car.add_widget(container)
    app.root.add_widget(car)
    app.root.add_widget(btn_2)

    return True


@run_in_app(app_class=CheckActionApp)
def test_checkbox():
    app = App.get_running_app()
    container = default_container()
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
    container = default_container()
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
    container = default_container()
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
    container_1 = default_container()
    to_screen_2 = FocusButton(text='To screen 2 ->')
    container_1.add_widget(to_screen_2)
    s1.add_widget(container_1)

    s2 = FocusScreen(name='screen_2')
    container_2 = default_container()
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
    container = default_container()
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


@run_in_app(app_class=CheckActionApp)
def test_tabbed_panel():
    app = App.get_running_app()
    app.step_1 = False
    container = default_container()
    instructions = Label(text='Press the button on the next tab, then press Submit.')
    tab_btn = FocusButton(text='Press me first')
    submit_btn = FocusButton(text='Submit', size_hint_y=0.1)

    inner_container = default_container()
    ignore_btn = FocusButton(text='Ignore me')
    inner_container.add_widget(instructions)
    inner_container.add_widget(ignore_btn)

    tp = FocusTabbedPanel()
    tp.default_tab_content = inner_container
    item = TabbedPanelItem(text='Go here')
    item.add_widget(tab_btn)
    tp.add_widget(item)

    def press_ignore(*args):    # Auto fail
        app.stop()


    def press_step_1(*args):
        app.step_1 = True


    def submit(*args):
        if app.step_1:
            app.did_action = True
            app.stop()

    ignore_btn.bind(on_press=press_ignore)
    tab_btn.bind(on_press=press_step_1)
    submit_btn.bind(on_press=submit)

    container.add_widget(tp)
    container.add_widget(submit_btn)

    app.root.add_widget(container)
    return True


@run_in_app(app_class=CheckActionApp)
def test_modal_view():
    app = App.get_running_app()
    container = default_container()

    def show_modal():
        view = FocusModalView(focus_return=container, auto_dismiss=False, size_hint=(0.5, 0.5))
        dismiss_btn = FocusButton(text='Dismiss this modal', on_press=lambda _: view.dismiss())
        view.add_widget(dismiss_btn)
        view.open()


    def submit(*args):
        app.did_action = True
        app.stop()

    submit_btn = FocusButton(text='Press this after dismissing the modal view', on_press=submit)
    container.add_widget(submit_btn)
    app.root.add_widget(container)
    Clock.schedule_once(lambda _: show_modal())
    return True


@run_in_app(app_class=CheckActionApp)
def test_popup():
    app = App.get_running_app()
    container = default_container()

    def show_popup():
        inner_container = default_container()
        dismiss_btn = FocusButton(text='Dismiss this popup')
        view = FocusPopup(title='Popup', content=inner_container, focus_return=container,
                            auto_dismiss=False, size_hint=(0.5, 0.5))
        dismiss_btn.bind(on_press=lambda *args: view.dismiss())
        inner_container.add_widget(dismiss_btn)
        view.open()


    def submit(*args):
        app.did_action = True
        app.stop()

    submit_btn = FocusButton(text='Press this after dismissing the popup', on_press=submit)
    container.add_widget(submit_btn)
    app.root.add_widget(container)
    Clock.schedule_once(lambda _: show_popup())
    return True


@run_in_app(app_class=CheckActionApp, timeout=20)
def test_accordion():
    app = App.get_running_app()
    app.step_1 = False

    instructions = Label(text='Navigate to the next accordion section.')
    step_1_btn = FocusButton(text='Press me first')
    submit_btn = FocusButton(text='Press me second')

    container_1 = default_container()
    container_1.add_widget(instructions)

    container_2 = default_container()
    container_2.add_widget(step_1_btn)

    acc = FocusAccordion()
    item_1 = FocusAccordionItem()
    item_1.add_widget(container_1)
    acc.add_widget(item_1)
    item_2 = FocusAccordionItem()
    item_2.add_widget(container_2)
    acc.add_widget(item_2)

    acc.select(item_1)

    container = default_container()
    container.add_widget(acc)
    container.add_widget(submit_btn)

    def step_1(*args):
        app.step_1 = True


    def submit(*args):
        if app.step_1:
            app.did_action = True
            app.stop()


    step_1_btn.bind(on_press=step_1)
    submit_btn.bind(on_press=submit)

    app.root.add_widget(container)
    return True


@run_in_app(app_class=CheckActionApp, timeout=25)
def test_scroll_view():
    app = App.get_running_app()
    instructions = Label(text='Look through the scroll area to find the correct button to press.', size_hint_y=0.1)
    correct_button = 'Button 3'

    scroll_container = FocusGridLayout(cols=10, size_hint=(None, None), size=(1000, 1000))
    for _ in range(99):
        scroll_container.add_widget(Label(text='Ignore me'))

    scroll_container.add_widget(Label(text=correct_button))

    button_container = FocusBoxLayout(orientation='horizontal', padding=10, spacing=10, size_hint_y=0.15)

    def guess(btn, *args):
        if btn.text == correct_button:
            app.did_action = True

        app.stop()

    for i in range(5):
        btn = FocusButton(text=f'Button {i}')
        btn.bind(on_press=guess)
        button_container.add_widget(btn)

    container = default_container()
    sv = FocusScrollView()
    sv.add_widget(scroll_container)
    for widg in (instructions, sv, button_container):
        container.add_widget(widg)

    app.root.add_widget(container)
    return True


class TreeViewFocusButton(FocusTreeViewNode, FocusButton):
    def __init__(self, **kwargs):
        FocusTreeViewNode.__init__(self, **kwargs)
        FocusButton.__init__(self, **kwargs)


@run_in_app(app_class=CheckActionApp, timeout=30)
def test_tree_view():
    app = App.get_running_app()
    app.step_1 = False
    instructions = Label(text='Press the first button under the first element, then the second button under the second element.', size_hint_y=0.1)

    tv = FocusTreeView(size_hint_y=0.9)
    node_1 = FocusTreeViewLabel(text='Go here first', size_hint_y=0.2)
    node_2 = FocusTreeViewLabel(text='Go here second', size_hint_y=0.2)
    btn_1 = TreeViewFocusButton(text='Press me first')
    btn_2 = TreeViewFocusButton(text='Press me second')
    fake_button = FocusButton(text='Ignore me')

    def step_1(*args):
        print('doing step 1')
        app.step_1 = True


    def submit(*args):
        print('doing step 2')
        if app.step_1:
            app.did_action = True
            app.stop()

    btn_1.bind(on_press=step_1)
    btn_2.bind(on_press=submit)

    tv.add_node(node_1)
    tv.add_node(node_2)
    tv.add_node(btn_1, node_1)
    tv.add_node(btn_2, node_2)

    container = default_container()
    container.add_widget(instructions)
    container.add_widget(tv)
    container.add_widget(fake_button)
    app.root.add_widget(container)
    return True
