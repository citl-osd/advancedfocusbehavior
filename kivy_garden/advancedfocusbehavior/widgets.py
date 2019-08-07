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

from behaviors import FocusWidget, FocusButtonBehavior, FocusToggleButtonBehavior


class FocusAccordion(FocusWidget, Accordion):
    """"""


# FocusActionBar and friends


class FocusButton(FocusButtonBehavior, FocusWidget, Button):
    """"""
    # This is probably complete as-is


class FocusCarousel(FocusWidget, Carousel):
    """"""


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


class FocusTextInput(TextInput):    # TextInput already uses FocusBehavior and highlights itself
    """"""


class FocusToggleButton(FocusWidget, FocusToggleButtonBehavior, ToggleButton):
    """"""


class FocusTreeView(FocusWidget, TreeView):
    """"""


# TreeViewNode


class FocusVideoPlayer(FocusWidget, VideoPlayer):
    """"""