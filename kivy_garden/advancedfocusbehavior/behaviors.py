"""
This module contains the critical new behaviors of Advanced Focus Behaviors.
"""

import kivy

kivy.require("1.11.1")

from pathlib import Path

from kivy.lang.builder import Builder

Builder.load_file(
    str(Path(__file__).parent.joinpath("advancedfocusbehaviors.kv").resolve())
)

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.accordion import AccordionItem
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior
from kivy.uix.carousel import Carousel
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from collections import deque
from itertools import chain
from math import sqrt


# Color constants
BACKGROUND = (0, 0, 0, 1)  # Black
HIGHLIGHT = (0.4471, 0.7765, 0.8118, 1)  # Blue


def link_focus(focusables, loopback=False):
    """
    Create a focus chain for a list of focusable widgets, such that each widget's
    :attr:`FocusBehavior.focus_previous` is the previous widget in the list, and each
    widget's :attr:`FocusBehavior.focus_next` is the next widget in the list.

    :param focusables: Widgets to link focus for.
    :type focusables: :class:`list`[:class:`FocusBehavior`]
    :param loopback: If :data:`True`, the first and last elements of :paramref:`focusables`
    will be linked.
    :type loopback: :class:`bool`
    """
    if len(focusables) <= 1:
        return

    prefix = focusables[-1] if loopback else None
    postfix = focusables[0] if loopback else None
    prev_iter = chain([prefix], focusables[:-1])
    next_iter = chain(focusables[1:], [postfix])
    for prev_w, curr_w, next_w in zip(prev_iter, focusables, next_iter):
        curr_w.focus_previous = prev_w
        curr_w.focus_next = next_w


class FocusAwareWidget(Widget):
    """
    A widget that cannot receive focus, but helps manage the focus of its children.
    """

    def __init__(self, **kwargs):
        self.focus_target = None
        super().__init__(**kwargs)

    def add_widget(self, widget, **kwargs):
        super().add_widget(widget, **kwargs)

        current_focus = self.find_focus_target()
        if not current_focus:

            if isinstance(widget, FocusWidget):
                widget.focus = True

            elif isinstance(widget, FocusAwareWidget) and widget.focus_target:
                self.set_focus_target(widget.focus_target)

    def remove_widget(self, widget):
        if hasattr(widget, "focus") and widget.focus:
            widget.focus = False

            focus_next = widget.get_focus_next()  # could also be prev
            if focus_next:
                focus_next.focus = True

        super().remove_widget(widget)

    def is_parent_aware(self):
        """
        Checks if the parent of this widget is focus aware.

        :return: :data:`True` if this widget's parent is focus aware, :data:`False` otherwise
        :rtype: :class:`bool`
        """
        return isinstance(self.parent, FocusAwareWidget)

    def find_focus_target(self):
        """
        Find the current focus target in the focus-aware portion of the widget tree.

        :return: Focus target
        :rtype: :class:`FocusWidget`
        """
        if self.focus_target:
            return self.focus_target

        if self.is_parent_aware():
            return self.parent.find_focus_target()

        return None

    def focus_first(self):
        """
        Focus the first widget in the widget tree that can receive focus, starting
        with this.

        :return: Newly focused widget, or :data:`None` if there was no widget that
        could receive focus.
        :rtype: :class:`Widget`
        """
        for widg in self.walk(loopback=True):
            if hasattr(widg, "focus"):
                widg.focus = True
                return widg

        return None

    def set_focus_target(self, new_target):
        """
        Set the focus target of this widget, as well as all of its focus-aware
        parents.

        :param new_target: New focus target.
        :type new_target: :class:`Widget`
        """
        if not (new_target and self.focus_target):
            self.focus_target = new_target

            if self.is_parent_aware():
                self.parent.set_focus_target(new_target)

    def set_focus_enabled(self, state):
        """
        Enable/disable focus for this widget and all widgets beneath it in the
        widget tree.

        :param state: New focus state. If :data:`True`, focus is enabled. If
            :data:`False`, focus is disabled.
        :type state: :class:`bool`
        """
        dq = deque()
        dq.append(self)
        last_focusable = None

        while dq:
            next_widget = dq.popleft()
            print(next_widget)
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

            elif state:  # get_focus_previous ignores self, which we want to focus
                last_focusable.focus = True

    def disable_focus(self):
        """
        Enables focus for this widget and all widgets beneath it in the widget
        tree. Shortcut for :meth:`set_focus_enabled`.
        """
        self.set_focus_enabled(False)

    def enable_focus(self):
        """
        Disables focus for this widget and all widgets beneath it in the widget
        tree. Shortcut for :meth:`set_focus_enabled`.
        """
        self.set_focus_enabled(True)


class FocusWidget(FocusBehavior, FocusAwareWidget):
    """
    A focusable :class:`Widget`.
    """

    def __init__(
        self,
        highlight_color=HIGHLIGHT,
        highlight_bg_color=BACKGROUND,
        draw_focus=True,
        **kwargs
    ):

        self.draw_focus = draw_focus
        self.highlight_color = highlight_color
        self.highlight_bg_color = highlight_bg_color
        super().__init__(**kwargs)
        self.bind(focus=self.focus_change)

    def focus_change(self, widg, focus):
        current = widg
        while isinstance(current.parent, Widget):
            if isinstance(current.parent, ScrollView):
                current.parent.scroll_to(widg)

            current = current.parent

        if focus:
            # Make sure that other focused widget, if it exists, gets defocused
            # first to maintain consistency in the FocusAware tree

            # TODO: speed this up, if possible
            for w in widg.walk_reverse(loopback=True):  # direction is arbitrary
                if w is not widg and getattr(w, "focus", False):
                    w.focus = False
                    break

        self.set_focus_target(self if focus else None)


class FocusButtonBehavior(ButtonBehavior, FocusBehavior):
    """
    Focus-enhanced version of :class:`ButtonBehavior`. Allows pressing buttons
    with the Enter key.
    """

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        if keycode[1] in ("enter", "numpadenter"):
            self.dispatch("on_press")
            return True

        return False

    def keyboard_on_key_up(self, window, keycode):
        if super().keyboard_on_key_up(window, keycode):
            return True

        if keycode[1] in ("enter", "numpadenter"):
            self.dispatch("on_release")
            return True

        return False


class FocusToggleButtonBehavior(FocusBehavior, ToggleButtonBehavior):
    """
    Focus-enhanced version of :class:`ToggleButtonBehavior`. Allows toggling with
    the Enter key.
    """

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        if keycode[1] in ("enter", "numpadenter"):
            self._do_press()
            return True

        return False


def mods_to_step_size(mods):
    """
    Convert a set of modifier keys to a step size.

    :param mods: Modifier keys.
    :type mods: :class:`tuple`[:class:`str`]
    :return: Step size, by name.
    :rtype: :class:`str`
    """
    if "alt" in mods:
        return "fine"

    elif "shift" in mods:
        return "coarse"

    return "medium"


def incr(value, max_val, step):
    return min(value + step, max_val)


def decr(value, min_val, step):
    return max(value - step, min_val)


def bfs_walk(widget):
    if not widget:
        return

    dq = deque()
    dq.append(widget)

    while dq:
        next_widget = dq.popleft()
        yield next_widget
        if isinstance(next_widget, Carousel):
            children = next_widget.slides

        elif isinstance(next_widget, ScreenManager):
            children = next_widget.screens

        elif isinstance(next_widget, AccordionItem):
            children = next_widget.container.children

        else:
            children = next_widget.children

        dq.extend(children)


class FocusApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self.check_focus)

    def check_focus(self, window, key, scancode, codepoint, modifier):
        if key != 9:  # Tab (TODO: find/create constant)
            return False

        first_focus = None
        for widg in bfs_walk(self.root):
            if hasattr(widg, "focus"):
                first_focus = widg

            if isinstance(widg, FocusAwareWidget) and widg.focus_target:
                return False

        if first_focus:
            first_focus.focus = True
            return True

        return False
