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
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior
from kivy.uix.widget import Widget


# Color constants
BACKGROUND = (0, 0, 0, 1)                   # Black
HIGHLIGHT = (0.4471, 0.7765, 0.8118, 1)     # Blue


class FocusAwareWidget:
    """"""
    def __init__(self, **kwargs):
        #super().__init__(**kwargs)
        self.focus_target = None


    def add_widget(self, widget, index=0, canvas=None):
        super().add_widget(widget, index, canvas)

        # No existing focused widget
        if not self.find_focus_target():

            # New widget can be focused; use it!
            if isinstance(widget, FocusWidget):
                widget.set_focus_target(widget)

            # New widget is an existing tree that has a focused element; use it!
            elif isinstance(widget, FocusAwareWidget) and widget.focus_target:
                self.set_focus_target(widget.focus_target)


        else:
            # We already have a focused widget. If the new tree has a focused
            # widget too, we need to defocus it.
            if isinstance(widget, FocusAwareWidget) and widget.focus_target:
                orig_target = widget.focus_target
                ptr = widget
                filter_func = lambda w: isinstance(w, FocusAwareWidget) and \
                                                w.focus_target is orig_target

                while ptr.focus_target is not ptr:
                    ptr.focus_target = None
                    ptr = next(filter(filter_func, ptr.children))

                # ptr is now widget being defocused
                ptr.focus_target = None
                ptr.focus = False


    def remove_widget(self, widget):
        if widget.focus:
            widget.focus = False

            for widg in widget.walk_reverse(loopback=True): # could also be walk?
                if widg is not widget and isinstance(widg, FocusWidget):
                    new_focus = widg
                    new_focus.set_focus_target(new_focus)
                    break

            else:
                self.set_focus_target(None)

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


    def set_focus_target(self, new_target):
        """"""
        self.focus_target = new_target
        if new_target is self:
            self.focus = True

        if self.is_parent_aware():
            self.parent.set_focus_target(new_target)


class FocusWidget(FocusBehavior, FocusAwareWidget):
    """"""

    def __init__(self, highlight_color=HIGHLIGHT, highlight_bg_color=BACKGROUND,
                 draw_focus=True, **kwargs):

        self.draw_focus = draw_focus
        self.highlight_color = highlight_color
        self.highlight_bg_color = highlight_bg_color

        FocusAwareWidget.__init__(self, **kwargs)
        #self.set_focus_target(self)
        #FocusBehavior.__init__(self, **kwargs)


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
