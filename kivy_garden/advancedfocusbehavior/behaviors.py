""""""

import kivy
kivy.require('1.11.1')

from pathlib import Path

from kivy.lang.builder import Builder
Builder.load_file(str(Path(__file__).parent.joinpath('advancedfocusbehaviors.kv').resolve()))

from kivy.app import App
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.graphics import Color, Rectangle
from kivy.uix.accordion import AccordionItem
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior
from kivy.uix.carousel import Carousel
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from collections import deque
from math import sqrt


# Color constants
BACKGROUND = (0, 0, 0, 1)                   # Black
HIGHLIGHT = (0.4471, 0.7765, 0.8118, 1)     # Blue


class FocusAwareWidget:
    """"""
    def __init__(self, **kwargs):
        #super().__init__(**kwargs)
        self.focus_target = None


    def add_widget(self, widget, **kwargs):
        super().add_widget(widget, **kwargs)

        # No existing focused widget
        current_focus = self.find_focus_target()
        if not current_focus:

            # New widget can be focused; use it!
            if isinstance(widget, FocusWidget):
                widget.focus = True
                #widget.set_focus_target(widget)

            # New widget is an existing tree that has a focused element; use it!
            elif isinstance(widget, FocusAwareWidget) and widget.focus_target:
                self.set_focus_target(widget.focus_target)


    def remove_widget(self, widget):
        if hasattr(widget, 'focus') and widget.focus:
            widget.focus = False

            focus_next = widget.get_focus_next()    # could also be prev
            if focus_next:
                focus_next.focus = True

        super().remove_widget(widget)


    def is_parent_aware(self):
        """"""
        return isinstance(self.parent, FocusAwareWidget)


    def find_focus_target(self):
        """"""
        if self.focus_target:
            return self.focus_target

        if self.is_parent_aware():
            return self.parent.find_focus_target()

        return None


    def focus_first(self):
        """"""
        for widg in self.walk(loopback=True):
            if hasattr(widg, 'focus'):
                widg.focus = True
                return widg

        return None


    def set_focus_target(self, new_target):
        """"""
        if not (new_target and self.focus_target):
            self.focus_target = new_target

            if self.is_parent_aware():
                self.parent.set_focus_target(new_target)


    def set_focus_enabled(self, state):
        """"""
        dq = deque()
        dq.append(self)
        last_focusable = None

        while dq:
            next_widget = dq.popleft()
            if isinstance(next_widget, FocusWidget):
                next_widget.is_focusable = state
                last_focusable = next_widget

            # A few widgets have their "children" in different places
            # TODO: check if there are other special cases
            if isinstance(next_widget, Carousel):
                children = next_widget.slides

            elif isinstance(next_widget, ScreenManager):
                children = next_widget.screens

            elif isinstance(next_widget, AccordionItem):
                children = next_widget.container.children

            else:
                children = next_widget.children

            dq.extend((c for c in children if isinstance(c, FocusAwareWidget)))

        if last_focusable and not self.find_focus_target():
            focus_next = last_focusable.get_focus_previous()
            if focus_next:
                focus_next.focus = True

            elif state:     # get_focus_previous ignores self, which we want to focus
                last_focusable.focus = True


    def disable_focus(self):
        self.set_focus_enabled(False)


    def enable_focus(self):
        self.set_focus_enabled(True)


class FocusWidget(FocusBehavior, FocusAwareWidget):
    """"""
    def __init__(self, highlight_color=HIGHLIGHT, highlight_bg_color=BACKGROUND,
                 draw_focus=True, **kwargs):

        self.draw_focus = draw_focus
        self.highlight_color = highlight_color
        self.highlight_bg_color = highlight_bg_color

        FocusAwareWidget.__init__(self, **kwargs)
        self.bind(focus=self.focus_change)

        if not hasattr(self, '_old_focus_next'):
            FocusBehavior.__init__(self, **kwargs)


    def focus_change(self, widg, focus):
        # TODO: assure that this widget is visible when it gains focus
        current = widg
        while isinstance(current.parent, Widget):
            if isinstance(current.parent, ScrollView):
                current.parent.scroll_to(widg)   # should this animate?

            current = current.parent

        if focus:
            # Make sure that other focused widget, if it exists, gets defocused
            # first to maintain consistency in the FocusAware tree

            # TODO: speed this up, if possible
            for w in widg.walk_reverse(loopback=True):  # direction is arbitrary
                if w is not widg and getattr(w, 'focus', False):
                    w.focus = False
                    break

        self.set_focus_target(self if focus else None)


class FocusButtonBehavior(ButtonBehavior, FocusBehavior):
    """"""
    def __init__(self, **kwargs):
        if not hasattr(self, '_old_focus_next'):
            FocusBehavior.__init__(self, **kwargs)

        ButtonBehavior.__init__(self, **kwargs)

        #self.bind(on_press=lambda *args: self.focus = True)


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


def mods_to_step_size(mods):
    """"""
    if 'alt' in mods:
        return 'fine'

    elif 'shift' in mods:
        return 'coarse'

    return 'medium'


def incr(value, max_val, step):
    """"""
    return min(value + step, max_val)


def decr(value, min_val, step):
    """"""
    return max(value - step, min_val)
