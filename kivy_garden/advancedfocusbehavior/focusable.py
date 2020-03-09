import kivy
kivy.require('1.11.1')

from kivy.factory import Factory

from kivy.event import EventDispatcher
from kivy.uix.accordion import Accordion
# TODO: action bar

from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.checkbox import CheckBox
from kivy.uix.codeinput import CodeInput
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.dropdown import DropDown
from kivy.uix.filechooser import FileChooser, FileChooserListView, FileChooserIconView, \
                                FileChooserController, FileChooserListLayout
from kivy.uix.label import Label
#from kivy.uix.modalview import ModalView
#from kivy.uix.popup import Popup
#from kivy.uix.pagelayout import PageLayout
# TODO: recycleview
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
# TODO: settings
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

from kivy_garden.advancedfocusbehavior.behaviors import FocusAwareWidget, \
            FocusWidget, FocusButtonBehavior, FocusToggleButtonBehavior, incr, \
            decr, mods_to_step_size


class FocusAccordion(FocusWidget, Accordion):
    """"""
    def __init__(self, **kwargs):
        FocusWidget.__init__(self, **kwargs)
        Accordion.__init__(self, **kwargs)


    def active_item(self):
        for i, child in enumerate(self.children):
            if not child.collapse:
                return i, child

        return None


    def select(self, instance):
        #print('calling select')
        super().select(instance)
        for child in self.children:
            if isinstance(child, FocusAwareWidget):
                child.set_focus_enabled(child is instance)


    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == 'tab' and 'ctrl' in modifiers:
            i, open_item = self.active_item()
            children = self.children

            if 'shift' in modifiers:    # Backwards
                if i < len(children) - 1:
                    self.select(children[i + 1])

                else:
                    self.select(children[0])

            else:                       # Forwards
                if i > 0:
                    self.select(children[i - 1])

                else:
                    self.select(children[-1])

            return True

        return super().keyboard_on_key_down(window, keycode, text, modifiers)


# FocusActionBar and friends


class FocusButton(FocusButtonBehavior, Button, FocusWidget):
    """"""
    def __init__(self, **kwargs):
        FocusWidget.__init__(self, **kwargs)
        FocusButtonBehavior.__init__(self, **kwargs)
        Button.__init__(self, **kwargs)


class FocusCarousel(FocusWidget, Carousel):
    """"""
    # (key, direction)
    keymap = {
        ('right', 'right'): 'next',
        ('right', 'left'): 'prev',
        ('left', 'right'): 'prev',
        ('left', 'left'): 'next',
        ('up', 'top'): 'next',
        ('up', 'bottom'): 'prev',
        ('down', 'top'): 'prev',
        ('down', 'bottom'): 'next'
    }


    def __init__(self, **kwargs):
        FocusWidget.__init__(self, **kwargs)
        Carousel.__init__(self, **kwargs)

        self.bind(current_slide=self.on_change_slide)


    def add_widget(self, widget, index=0, canvas=None):
        Carousel.add_widget(self, widget, index=index, canvas=canvas)
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
    """"""
    def __init__(self, **kwargs):
        FocusToggleButtonBehavior.__init__(self, **kwargs)
        FocusWidget.__init__(self, **kwargs)
        CheckBox.__init__(self, **kwargs)


# FocusCodeInput might not be feasible b/c it needs tabs
#class FocusCodeInput(FocusWidget, CodeInput)


class FocusColorPicker(FocusWidget, ColorPicker):
    """"""


# unnecessary; all focus functionality is encapsulated in children
#class FocusDropDown(FocusWidget, DropDown):
#    """"""


class FocusFileChooser(FocusWidget, FileChooser):
    """"""


class FocusFileChooserListView(FocusWidget, FileChooserListView):
    """"""


class FocusFileChooserIconView(FocusWidget, FileChooserIconView):
    """"""


class FocusScreen(FocusWidget, Screen):
    """"""


# settings


class FocusScrollView(FocusWidget, ScrollView):
    """"""
    scroll_dist = 20    # TODO: base this on dpi instead?

    def __init__(self, **kwargs):
        FocusWidget.__init__(self, **kwargs)
        ScrollView.__init__(self, **kwargs)


    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        key = keycode[1]
        scroll_dist_x, scroll_dist_y = self.convert_distance_to_scroll(self.scroll_dist, self.scroll_dist)

        if key == 'up':
            self.scroll_y = incr(self.scroll_y, 1, scroll_dist_y)

        elif key == 'down':
            self.scroll_y = decr(self.scroll_y, 0, scroll_dist_y)

        elif key == 'right':
            self.scroll_x = incr(self.scroll_x, 1, scroll_dist_x)

        elif key == 'left':
            self.scroll_x = decr(self.scroll_x, 0, scroll_dist_x)

        else:
            return False

        return True


class FocusSlider(FocusWidget, Slider):
    """

    controls:
        +/- to increase/decrease value
        hold shift to decrese sensitivity
        hold alt to increase sensitivity
    """
    def __init__(self, fine_control=None, medium_control=None, coarse_control=None, **kwargs):
        FocusWidget.__init__(self, **kwargs)
        Slider.__init__(self, **kwargs)

        slider_range = self.max - self.min
        self.control_map = {
            'fine': fine_control or min(1, slider_range / 100),
            'medium': medium_control or sqrt(slider_range / 5),
            'coarse': coarse_control or slider_range / 5
        }


    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        key = keycode[1]
        if key not in ('=', '-'):
            return False

        step = self.control_map[mods_to_step_size(modifiers)]

        if key == '=':
            self.value = incr(self.value, self.max, step)

        else:
            self.value = decr(self.value, self.min, step)

        return True


class FocusSpinner(FocusWidget, Spinner):
    """"""


class FocusSwitch(FocusWidget, Switch):
    def __init__(self, **kwargs):
        FocusWidget.__init__(self, **kwargs)
        Switch.__init__(self, **kwargs)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        key = keycode[1]
        if key in ('enter', 'numpadenter'):
            self.active = not self.active
            return True

        return super().keyboard_on_key_down(window, keycode, text, modifiers)


class FocusTabbedPanel(FocusWidget, TabbedPanel):
    """"""
    def __init__(self, **kwargs):
        FocusWidget.__init__(self, **kwargs)
        TabbedPanel.__init__(self, **kwargs)


    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == 'tab' and 'ctrl' in modifiers:
            tab_list = self.tab_list
            current_tab = self.current_tab
            current_idx = tab_list.index(current_tab)

            if 'shift' in modifiers:    # Backwards
                if current_idx < len(tab_list) - 1:
                    self.switch_to(tab_list[current_idx + 1])

                else:
                    self.switch_to(tab_list[0])

            else:                       # Forwards
                if current_idx > 0:
                    self.switch_to(tab_list[current_idx - 1])

                else:
                    self.switch_to(tab_list[-1])

            return True

        return super().keyboard_on_key_down(window, keycode, text, modifiers)


class FocusTextInput(FocusWidget, TextInput):   # TextInput already uses FocusBehavior and highlights itself
    """"""
    def __init__(self, **kwargs):
        self.draw_focus = False
        TextInput.__init__(self, write_tab=False, **kwargs)
        FocusWidget.__init__(self, draw_focus=False, **kwargs)


class FocusToggleButton(FocusToggleButtonBehavior, FocusWidget, ToggleButton):
    """"""
    def __init__(self, **kwargs):
        FocusToggleButtonBehavior.__init__(self, **kwargs)
        FocusWidget.__init__(self, **kwargs)
        ToggleButton.__init__(self, **kwargs)


class FocusTreeView(FocusAwareWidget, TreeView):
    """"""
    def __init__(self, **kwargs):
        FocusAwareWidget.__init__(self, **kwargs)
        TreeView.__init__(self, **kwargs)

    def add_node(self, node, parent=None):
        n = super().add_node(node, parent)
        n.tree = weakref.proxy(self)
        return n

    def remove_node(self, node):
        super().remove_node(node)
        node.tree = None

    def _do_layout(self, tree_node):
        print(f'outer _do_layout {self}')
        focus_return = None
        for node in self.iterate_open_nodes():
            if hasattr(node, 'focus') and node.focus:
                focus_return = node
                break

        super()._do_layout(tree_node)
        if focus_return:
            focus_return.focus = True

Factory.register('FocusTreeView', cls=FocusTreeView)


class FocusTreeViewNode(TreeViewNode, FocusWidget):
    """"""
    def __init__(self, **kwargs):
        if self.__class__ is FocusTreeViewNode:
            raise TreeViewException('You cannot use FocusTreeViewNode directly.')

        if hasattr(self, 'focus'):
            self.bind(is_selected=self._set_focus)

        super().__init__(**kwargs)

    def _set_focus(self, widg, val):
        self.is_focusable = val

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        key = keycode[1]
        if key in ('enter', 'numpadenter'):
            self.tree.toggle_node(self)
            self.tree.select_node(self)
            return True

        return False

Factory.register('FocusTreeViewNode', cls=FocusTreeViewNode)


class FocusTreeViewLabel(Label, FocusTreeViewNode):
    pass


class FocusVideoPlayer(FocusWidget, VideoPlayer):
    """"""
    def __init__(self, fine_control=None, medium_control=None, coarse_control=None,
                    volume_interval=0.2, **kwargs):
        FocusWidget.__init__(self, **kwargs)
        VideoPlayer.__init__(self, **kwargs)
        self.volume_interval = volume_interval
        self.fine_control = fine_control
        self.medium_control = medium_control
        self.coarse_control = coarse_control

        self.bind(duration=self.set_control_map)


    def set_control_map(self, *args):
        self.control_map = {
            'fine': self.fine_control or min(1, self.duration / 100),
            'medium': self.medium_control or int(sqrt(self.duration / 5)),
            'coarse': self.coarse_control or (self.duration // 5)
        }


    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        key = keycode[1]

        # Pause/Play
        if key == 'spacebar':
            self.state = 'pause' if self.state == 'play' else 'play'

        # Volume
        elif key == '=':
            self.volume = min(self.volume + self.volume_interval, 1)

        elif key == '-':
            self.volume = max(self.volume - self.volume_interval, 0)

        # Seeking
        elif key in (']', '['):

            # Video hasn't loaded; don't try to seek through it
            if self.duration == -1:
                return False

            step = self.control_map[mods_to_step_size(modifiers)]

            if key == ']':
                self.position = incr(self.position, self.duration, step)

            else:
                self.position = decr(self.position, 0, step)

        # A key we don't care about
        else:
            return False

        return True


class FocusFileChooserListView(FileChooserController):
    _ENTRY_TEMPLATE = 'FocusFileListEntry'

Factory.register('FocusFileChooserListView', cls=FocusFileChooserListView)


class FocusFileChooserListLayout(FileChooserListLayout):
    VIEWNAME = 'focuslist'
    _ENTRY_TEMPLATE = 'FocusFileListEntry'

Factory.register('FocusFileChooserListLayout', cls=FocusFileChooserListLayout)
