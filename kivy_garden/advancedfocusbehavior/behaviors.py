""""""

import kivy
kivy.require('1.11.1')

from pathlib import Path

from kivy.lang.builder import Builder
Builder.load_file(str(Path(__file__).parent.joinpath('advancedfocusbehaviors.kv').resolve()))

from kivy.event import EventDispatcher
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior
from kivy.uix.widget import Widget

from kivy_garden.advancedfocusbehavior.misc import find_first_focused


# Color constants
BACKGROUND = (0, 0, 0, 1)                   # Black
HIGHLIGHT = (0.4471, 0.7765, 0.8118, 1)     # Blue


# TODO: move this to widgets
class FocusWidget(FocusBehavior, Widget):
    """"""

    def __init__(self, highlight_color=HIGHLIGHT, background_color=BACKGROUND, **kwargs):
        Widget.__init__(self, **kwargs)
        self.highlight_color = highlight_color
        self.background_color = background_color

        self.bind(focus=self.focus_change, parent=self.check_for_focused_widget)


    def check_for_focused_widget(self, *args):
        if not find_first_focused(self):
            self.focus = True


    def focus_change(self, *args):
        # TODO: assure that this widget is visible when it gains focus
        pass


class FocusButtonBehavior(FocusBehavior, ButtonBehavior, EventDispatcher):
    """"""
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        if keycode[1] in ('enter', 'numpadenter'):
            self.dispatch('on_press')
            return True

        return False


class FocusToggleButtonBehavior(FocusBehavior, ToggleButtonBehavior, EventDispatcher):
    """"""
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        if keycode[1] in ('enter', 'numpadenter'):
            self._do_press()
            return True

        return False
