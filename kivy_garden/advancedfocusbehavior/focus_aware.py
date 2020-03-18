"""
This module contains a variety of focus-aware widgets, meaning that, while they
cannot receive focus, they help manage the focus of widgets beneath them.
"""


import kivy

kivy.require("1.11.1")

from kivy.uix.accordion import AccordionItem
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.pagelayout import PageLayout
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatter import Scatter
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy_garden.advancedfocusbehavior.behaviors import (
    FocusAwareWidget,
    FocusWidget,
    link_focus,
)


class FocusAccordionItem(FocusAwareWidget, AccordionItem):
    """
    Focus-aware :class:`AccordionItem`.
    """


class FocusAnchorLayout(FocusAwareWidget, AnchorLayout):
    """
    Focus-aware :class:`AnchorLayout`.
    """


class FocusBoxLayout(FocusAwareWidget, BoxLayout):
    """
    Focus-aware :class:`BoxLayout`.
    """


class FocusFloatLayout(FocusAwareWidget, FloatLayout):
    """
    Focus-aware :class:`FloatLayout`.
    """


class FocusGridLayout(FocusAwareWidget, GridLayout):
    """
    Focus-aware :class:`GridLayout`.
    """


class FocusModalView(FocusAwareWidget, ModalView):
    """
    Focus-aware :class:`ModalView`.
    """

    def __init__(self, focus_return=None, **kwargs):
        super().__init__(**kwargs)
        self.focus_return = focus_return

        self.bind(on_dismiss=self.lose_focus)

    def lose_focus(self, *args):
        focus_return = self.focus_return
        if focus_return:
            focus_return.focus_first()


class FocusPageLayout(FocusAwareWidget, PageLayout):
    """
    Focus-aware :class:`PageLayout`.
    """


class FocusPopup(FocusModalView, Popup):
    """
    Focus-aware :class:`Popup`.
    """

    def __init__(self, focus_return=None, **kwargs):
        kwargs["focus_return"] = focus_return
        super().__init__(**kwargs)


class FocusRelativeLayout(FocusAwareWidget, RelativeLayout):
    """
    Focus-aware :class:`RelativeLayout`.
    """


class FocusScatterLayout(FocusAwareWidget, ScatterLayout):
    """
    Focus-aware :class:`ScatterLayout`.
    """


class FocusStackLayout(FocusAwareWidget, StackLayout):
    """
    Focus-aware :class:`StackLayout`.
    """


class FocusScatter(FocusAwareWidget, Scatter):
    """
    Focus-aware :class:`Scatter`.
    """


class FocusScreenManager(FocusAwareWidget, ScreenManager):
    """
    Focus-aware :class:`ScreenManager`.
    """

    def add_widget(self, screen):
        super().add_widget(screen)
        if len(self.screens) == 1:
            self.current_screen.focus_first()

    def on_change_screen(self, manager, new_screen):
        for s in self.screens:
            if s is not new_screen and isinstance(s, FocusAwareWidget):
                s.disable_focus()

        if isinstance(new_screen, FocusAwareWidget):
            new_screen.enable_focus()


class FocusScreen(FocusAwareWidget, Screen):
    """
    Focus-aware :class:`Screen`.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_enter=self.focus_first)

    def focus_first(self, *args):
        for widg in self.walk():
            if isinstance(widg, FocusWidget):
                widg.focus = True
                break


class FocusDropDown(FocusAwareWidget, DropDown):
    """
    Focus-aware :class:`DropDown`.
    """

    def open(self, widget):
        super().open(widget)
        print("got opened")
        link_focus(list(reversed(self.children[0].children)))
        print(self.children[0].children)
        for child in self.children[0].children:
            child.enable_focus()

    def dismiss(self, *args):
        super().dismiss(*args)
        print("got dismissed")
        for child in self.children[0].children:
            child.disable_focus()   # BUG: this hangs when an option is selected

        print("disabled focus")
