"""
This module contains focus-enabled versions of most of the base widgets in Kivy.
"""


import kivy

kivy.require("1.11.1")

from kivy.factory import Factory

from kivy.uix.accordion import Accordion

from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.checkbox import CheckBox
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.filechooser import (
    FileChooser,
    FileChooserListView,
    FileChooserIconView,
    FileChooserController,
    FileChooserListLayout,
)
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.treeview import TreeView, TreeViewNode
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.widget import Widget

from math import sqrt
import weakref

from kivy_garden.advancedfocusbehavior.behaviors import (
    FocusAwareWidget,
    FocusWidget,
    FocusButtonBehavior,
    FocusToggleButtonBehavior,
    incr,
    decr,
    mods_to_step_size,
)


class FocusTextInput(FocusWidget, TextInput):
    """
    Focusable :class:`TextInput`.
    """

    def __init__(self, **kwargs):
        kwargs["write_tab"] = False
        kwargs["draw_focus"] = False
        super().__init__(**kwargs)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        # There is currently a bug in Kivy where modifiers gets converted from
        # a list to a set in TextInput's keyboard_on_key_down before being sent
        # to FocusBehavior's keyboard_on_key_down, and currently, the check for
        # shift is implemented weirdly (it does ["shift"]==modifiers instead of
        # "shift" in modifiers). If that gets fixed by Kivy in the future, this
        # function can be deleted in its entirety.
        if keycode[1] == "tab" and "shift" in modifiers:
            next = self.get_focus_previous()
            if next:
                self.focus = False
                next.focus = True

            return True

        return super().keyboard_on_key_down(window, keycode, text, modifiers)


class FocusAccordion(FocusWidget, Accordion):
    """
    Focusable :class:`Accordion`.

    While focused, the accordion can be cycled forward by pressing Ctrl+Tab, and
    backward by pressing Shift+Ctrl+Tab.
    """

    def active_item(self):
        for i, child in enumerate(self.children):
            if not child.collapse:
                return i, child

        return None

    def select(self, instance):
        super().select(instance)
        for child in self.children:
            if isinstance(child, FocusAwareWidget):
                child.set_focus_enabled(child is instance)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == "tab" and "ctrl" in modifiers:
            i, open_item = self.active_item()
            children = self.children

            if "shift" in modifiers:  # Backwards
                if i < len(children) - 1:
                    self.select(children[i + 1])

                else:
                    self.select(children[0])

            else:  # Forwards
                if i > 0:
                    self.select(children[i - 1])

                else:
                    self.select(children[-1])

            return True

        return super().keyboard_on_key_down(window, keycode, text, modifiers)


class FocusButton(FocusButtonBehavior, Button, FocusWidget):
    """
    Focusable :class:`Button`.
    """


class FocusCarousel(FocusWidget, Carousel):
    """
    Focusable :class:`Carousel`.

    While focused, the carousel can be navigated using the arrow keys.
    """

    # (key, direction)
    keymap = {
        ("right", "right"): "next",
        ("right", "left"): "prev",
        ("left", "right"): "prev",
        ("left", "left"): "next",
        ("up", "top"): "next",
        ("up", "bottom"): "prev",
        ("down", "top"): "prev",
        ("down", "bottom"): "next",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(current_slide=self.on_change_slide)

    def add_widget(self, widget, index=0, canvas=None):
        super().add_widget(widget, index=index, canvas=canvas)
        if len(self.slides) > 1 and isinstance(widget, FocusAwareWidget):
            widget.disable_focus()

    def on_change_slide(self, carousel, slide):
        if isinstance(slide, FocusAwareWidget):
            slide.enable_focus()

        for s in self.slides:
            if s is not slide and isinstance(s, FocusAwareWidget):
                s.disable_focus()

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        load_type = FocusCarousel.keymap.get((keycode[1], self.direction))

        if load_type:
            self.load_next(mode=load_type)
            return True

        return False


class FocusCheckBox(FocusToggleButtonBehavior, FocusWidget, CheckBox):
    """
    Focusable :class:`CheckBox`.
    """


class FocusColorPicker_Input(FocusTextInput):
    def __init__(self, **kwargs):
        print("FocusColorPicker_Input constructor")
        super().__init__(**kwargs)


class FocusColorPicker(FocusAwareWidget, ColorPicker):
    """
    Focusable :class:`ColorPicker`.
    """


class FocusFileChooser(FocusWidget, FileChooser):
    """"""


class FocusFileChooserListView(FocusWidget, FileChooserListView):
    """"""


class FocusFileChooserIconView(FocusWidget, FileChooserIconView):
    """"""


class FocusScrollView(FocusWidget, ScrollView):
    """
    Focusable :class:`ScrollView`.

    While focused, the scoll view can be scrolled with the arrow keys.
    """

    scroll_dist = 20  # TODO: base this on dpi instead?

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        key = keycode[1]
        scroll_dist_x, scroll_dist_y = self.convert_distance_to_scroll(
            self.scroll_dist, self.scroll_dist
        )

        if key == "up":
            self.scroll_y = incr(self.scroll_y, 1, scroll_dist_y)
            return True

        elif key == "down":
            self.scroll_y = decr(self.scroll_y, 0, scroll_dist_y)
            return True

        elif key == "right":
            self.scroll_x = incr(self.scroll_x, 1, scroll_dist_x)
            return True

        elif key == "left":
            self.scroll_x = decr(self.scroll_x, 0, scroll_dist_x)
            return True

        return False


class FocusSlider(FocusWidget, Slider):
    """
    Focusable :class:`Slider`.

    While focused, the slider can be adjusted with the + and - keys. Hold the Alt
    key for fine control. Hold the Shift key for coarse control.
    """

    def __init__(
        self, fine_control=None, medium_control=None, coarse_control=None, **kwargs
    ):
        super().__init__(**kwargs)

        slider_range = self.max - self.min
        self.control_map = {
            "fine": fine_control or min(1, slider_range / 100),
            "medium": medium_control or sqrt(slider_range / 5),
            "coarse": coarse_control or slider_range / 5,
        }

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        key = keycode[1]
        if key not in ("=", "-"):
            return False

        step = self.control_map[mods_to_step_size(modifiers)]

        if key == "=":
            self.value = incr(self.value, self.max, step)

        else:
            self.value = decr(self.value, self.min, step)

        return True


class FocusSpinner(FocusWidget, Spinner):
    """"""


class FocusSwitch(FocusWidget, Switch):
    """
    Focusable :class:`Switch`.

    While focused, the switch can be toggled with the Enter key.
    """

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        key = keycode[1]
        if key in ("enter", "numpadenter"):
            self.active = not self.active
            return True

        return super().keyboard_on_key_down(window, keycode, text, modifiers)


class FocusTabbedPanel(FocusWidget, TabbedPanel):
    """
    Focusable :class:`TabbedPanel`.

    While focused, the active tab can be cycled forward with Ctrl+Tab and
    backward with Shift+Ctrl+Tab.
    """

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == "tab" and "ctrl" in modifiers:
            tab_list = self.tab_list
            current_tab = self.current_tab
            current_idx = tab_list.index(current_tab)

            if "shift" in modifiers:  # Backwards
                if current_idx < len(tab_list) - 1:
                    self.switch_to(tab_list[current_idx + 1])

                else:
                    self.switch_to(tab_list[0])

            else:  # Forwards
                if current_idx > 0:
                    self.switch_to(tab_list[current_idx - 1])

                else:
                    self.switch_to(tab_list[-1])

            return True

        return super().keyboard_on_key_down(window, keycode, text, modifiers)


class FocusToggleButton(FocusToggleButtonBehavior, FocusWidget, ToggleButton):
    """
    Focusable :class:`ToggleButton`.
    """


class FocusTreeView(FocusAwareWidget, TreeView):
    """
    Focus-aware :class:`TreeView`.
    """

    def add_node(self, node, parent=None):
        n = super().add_node(node, parent)
        n.tree = weakref.proxy(self)
        return n

    def remove_node(self, node):
        super().remove_node(node)
        node.tree = None

    def _do_layout(self, tree_node):
        print(f"outer _do_layout {self}")
        focus_return = None
        for node in self.iterate_open_nodes():
            if hasattr(node, "focus") and node.focus:
                focus_return = node
                break

        super()._do_layout(tree_node)
        if focus_return:
            focus_return.focus = True


Factory.register("FocusTreeView", cls=FocusTreeView)


class FocusTreeViewNode(TreeViewNode, FocusWidget):
    """
    Focusable :class:`TreeViewNode`. Like :class:`TreeViewNode`, this must be
    subclassed and cannot be instantiated on its own.
    """

    def __init__(self, **kwargs):
        if self.__class__ is FocusTreeViewNode:
            raise TreeViewException("You cannot use FocusTreeViewNode directly.")

        if hasattr(self, "focus"):
            self.bind(is_selected=self._set_focus)

        super().__init__(**kwargs)

    def _set_focus(self, widg, val):
        self.is_focusable = val

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        key = keycode[1]
        if key in ("enter", "numpadenter"):
            self.tree.toggle_node(self)
            self.tree.select_node(self)
            return True

        return False


Factory.register("FocusTreeViewNode", cls=FocusTreeViewNode)


class FocusTreeViewLabel(Label, FocusTreeViewNode):
    pass


class FocusVideoPlayer(FocusWidget, VideoPlayer):
    """
    Focusable :class:`VideoPlayer`.

    While focused, the following controls are available:

    - Play/pause with Space
    - Increase/decrease volume with +/-
    - Seek forward/backward in the video with ] and [. Hold Shift to seek faster
        and Alt to seek slower.
    """

    def __init__(
        self,
        fine_control=None,
        medium_control=None,
        coarse_control=None,
        volume_interval=0.2,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.volume_interval = volume_interval
        self.fine_control = fine_control
        self.medium_control = medium_control
        self.coarse_control = coarse_control

        self.bind(duration=self.set_control_map)

    def set_control_map(self, *args):
        self.control_map = {
            "fine": self.fine_control or min(1, self.duration / 100),
            "medium": self.medium_control or int(sqrt(self.duration / 5)),
            "coarse": self.coarse_control or (self.duration // 5),
        }

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        key = keycode[1]

        # Pause/Play
        if key == "spacebar":
            self.state = "pause" if self.state == "play" else "play"
            return True

        # Volume
        elif key == "=":
            self.volume = min(self.volume + self.volume_interval, 1)
            return True

        elif key == "-":
            self.volume = max(self.volume - self.volume_interval, 0)
            return True

        # Seeking
        elif key in ("]", "["):

            # Video hasn't loaded; don't try to seek through it
            if self.duration == -1:
                return False

            step = self.control_map[mods_to_step_size(modifiers)]

            if key == "]":
                self.position = incr(self.position, self.duration, step)

            else:
                self.position = decr(self.position, 0, step)

            return True

        return False


class FocusFileChooserListView(FileChooserController):
    _ENTRY_TEMPLATE = "FocusFileListEntry"


Factory.register("FocusFileChooserListView", cls=FocusFileChooserListView)


class FocusFileChooserListLayout(FileChooserListLayout):
    VIEWNAME = "focuslist"
    _ENTRY_TEMPLATE = "FocusFileListEntry"


Factory.register("FocusFileChooserListLayout", cls=FocusFileChooserListLayout)
