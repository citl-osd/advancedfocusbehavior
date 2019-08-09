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

from kivy_garden.advancedfocusbehavior.behaviors import FocusWidget, FocusButtonBehavior, FocusToggleButtonBehavior


class FocusAccordion(FocusWidget, Accordion):
    """"""


# FocusActionBar and friends


class FocusButton(FocusButtonBehavior, Button, FocusWidget):
    """"""
    def __init__(self, **kwargs):
        FocusButtonBehavior.__init__(self, **kwargs)
        FocusWidget.__init__(self, **kwargs)
        Button.__init__(self, **kwargs)


class FocusCarousel(FocusWidget, Carousel):
    """"""
    def key_to_load_type(self, key):
        """"""


    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if super().keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        load_type = self.key_to_load_type(keycode[1])

        if load_type:
            self.load_next(mode=load_type)
            return True

        return False


class FocusCheckBox(FocusToggleButtonBehavior, FocusWidget, CheckBox):
    """"""


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
    """"""


class FocusSpinner(FocusWidget, Spinner):
    """"""


class FocusTabbedPanel(FocusWidget, TabbedPanel):
    """"""


class FocusTextInput(FocusWidget, TextInput):   # TextInput already uses FocusBehavior and highlights itself
    """"""
    def __init__(self, **kwargs):
        kwargs.pop('focus', None)
        TextInput.__init__(self, **kwargs)
        FocusWidget.__init__(self, **kwargs)


class FocusToggleButton(FocusWidget, FocusToggleButtonBehavior, ToggleButton):
    """"""


class FocusTreeView(FocusWidget, TreeView):
    """"""


# TreeViewNode


class FocusVideoPlayer(FocusWidget, VideoPlayer):
    """"""
