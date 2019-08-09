""""""

import kivy
kivy.require('1.11.1')

from pathlib import Path

from kivy.lang.builder import Builder
Builder.load_file(str(Path(__file__).parent.joinpath('advancedfocusbehaviors.kv').resolve()))

from kivy.app import App
from kivy.event import EventDispatcher
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior
from kivy.uix.widget import Widget

from kivy_garden.advancedfocusbehavior.misc import find_first_focused, focus_first


# Color constants
BACKGROUND = (0, 0, 0, 1)                   # Black
HIGHLIGHT = (0.4471, 0.7765, 0.8118, 1)     # Blue


class FocusApp(App):
    """"""
    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, r):
        self._root = r
        if r:
            focus_first(r)


# TODO: move this to widgets
class FocusWidget(FocusBehavior, Widget):
    """"""

    def __init__(self, highlight_color=HIGHLIGHT, highlight_bg_color=BACKGROUND, **kwargs):
        Widget.__init__(self, **kwargs)
        #FocusBehavior.__init__(self, **kwargs)
        self.highlight_color = highlight_color
        self.highlight_bg_color = highlight_bg_color

        self.bind(parent=self.check_for_focused_widget)


    def check_for_focused_widget(self, *args):
        self.focus = not bool(find_first_focused(self))


    def focus_change(self, *args):
        # TODO: assure that this widget is visible when it gains focus
        print(f'focus change: {self.focus}, disabled: {self.disabled}, focusable: {self.is_focusable}')


class FocusButtonBehavior(ButtonBehavior, FocusBehavior):
    """"""
    def __init__(self, **kwargs):
        FocusBehavior.__init__(self, **kwargs)
        ButtonBehavior.__init__(self, **kwargs)


    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        if keycode[1] in ('enter', 'numpadenter'):
            self.dispatch('on_press')
            return True

        return False


class FocusToggleButtonBehavior(FocusBehavior, ToggleButtonBehavior):
    """"""
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        if keycode[1] in ('enter', 'numpadenter'):
            self._do_press()
            return True

        return False
