import kivy
kivy.require('1.11.1')

from kivy.uix.accordion import Accordion
# TODO: action bar

from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.checkbox import CheckBox
from kivy.uix.codeinput import CodeInput
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.dropdown import DropDown
from kivy.uix.filechooser import FileChooser, FileChooserListView, FileChooserIconView
from kivy.uix.modalview import ModalView
from kivy.uix.pagelayout import PageLayout
# TODO: recycleview
from kivy.uix.screenmanager import Screen
# TODO: settings
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.treeview import TreeView, TreeViewNode
from kivy.uix.videoplayer import VideoPlayer

from kivy_garden.advancedfocusbehavior.behaviors import FocusAwareWidget, \
            FocusWidget, FocusButtonBehavior, FocusToggleButtonBehavior

from math import sqrt


class FocusAccordion(FocusWidget, Accordion):
    """"""


# FocusActionBar and friends


class FocusButton(FocusButtonBehavior, Button, FocusWidget):
    """"""
    def __init__(self, **kwargs):
        FocusWidget.__init__(self, **kwargs)
        FocusButtonBehavior.__init__(self, **kwargs)
        Button.__init__(self, **kwargs)


class FocusCarousel(FocusWidget, Carousel):
    """"""
    def __init__(self, **kwargs):
        FocusWidget.__init__(self, **kwargs)
        Carousel.__init__(self, **kwargs)

        self.bind(current_slide=self.on_change_slide)


    def on_change_slide(self, carousel, slide):
        if isinstance(slide, FocusAwareWidget):
            slide.enable_focus()

        for s in self.slides:
            if s is not slide and isinstance(s, FocusAwareWidget):
                s.disable_focus()

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


    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        #print(keycode)
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


class FocusDropDown(FocusWidget, DropDown):
    """"""


class FocusFileChooser(FocusWidget, FileChooser):
    """"""


class FocusFileChooserListView(FocusWidget, FileChooserListView):
    """"""


class FocusFileChooserIconView(FocusWidget, FileChooserIconView):
    """"""


class FocusModalView(FocusWidget, ModalView):
    """"""


# pagelayout


class FocusScreen(FocusWidget, Screen):
    """"""


# settings


class FocusSlider(FocusWidget, Slider):
    """

    controls:
        +/- to increase/decrease value
        hold shift to decrese sensitivity
        hold alt to increase sensitivity
    """
    def __init__(self, fine_control=1.0, **kwargs):
        FocusWidget.__init__(self, **kwargs)
        Slider.__init__(self, **kwargs)
        self.fine_control = fine_control


    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        key = keycode[1]
        if key not in ('=', '-'):
            return False

        slider_range = self.max - self.min

        if 'alt' in modifiers:  # Fine control
            step = self.fine_control

        elif 'shift' in modifiers:  # Coarse control
            step = slider_range / 5

        else:   # Just right control
            step = sqrt(slider_range // 5)

        if key == '=':
            self.value = min(self.value + step, self.max)

        else:
            self.value = max(self.value - step, self.min)

        return True


class FocusSpinner(FocusWidget, Spinner):
    """"""


class FocusTabbedPanel(FocusWidget, TabbedPanel):
    """"""


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


class FocusTreeView(FocusWidget, TreeView):
    """"""


# TreeViewNode


class FocusVideoPlayer(FocusWidget, VideoPlayer):
    """"""
