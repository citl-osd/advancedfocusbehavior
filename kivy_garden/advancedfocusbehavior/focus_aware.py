import kivy
kivy.require('1.11.1')

from kivy.uix.accordion import AccordionItem
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.pagelayout import PageLayout
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy_garden.advancedfocusbehavior.behaviors import FocusAwareWidget, FocusWidget


class FocusAccordionItem(FocusAwareWidget, AccordionItem):
    """"""
    def __init__(self, **kwargs):
        FocusAwareWidget.__init__(self, **kwargs)
        AccordionItem.__init__(self, **kwargs)


class FocusAnchorLayout(FocusAwareWidget, AnchorLayout):
    """"""
    def __init__(self, **kwargs):
        AnchorLayout.__init__(self, **kwargs)
        FocusAwareWidget.__init__(self, **kwargs)


class FocusBoxLayout(FocusAwareWidget, BoxLayout):
    """"""
    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)
        FocusAwareWidget.__init__(self, **kwargs)


class FocusFloatLayout(FocusAwareWidget, FloatLayout):
    """"""
    def __init__(self, **kwargs):
        FloatLayout.__init__(self, **kwargs)
        FocusAwareWidget.__init__(self, **kwargs)


class FocusGridLayout(FocusAwareWidget, GridLayout):
    """"""
    def __init__(self, **kwargs):
        GridLayout.__init__(self, **kwargs)
        FocusAwareWidget.__init__(self, **kwargs)


class FocusModalView(FocusAwareWidget, ModalView):
    """"""
    def __init__(self, focus_return=None, **kwargs):
        FocusAwareWidget.__init__(self, **kwargs)
        ModalView.__init__(self, **kwargs)
        self.focus_return = focus_return

        self.bind(on_dismiss=self.lose_focus)


    def lose_focus(self, *args):
        focus_return = self.focus_return
        if focus_return:
            focus_return.focus_first()


class FocusPageLayout(FocusAwareWidget, PageLayout):
    """"""
    def __init__(self, **kwargs):
        PageLayout.__init__(self, **kwargs)
        FocusAwareWidget.__init__(self, **kwargs)


class FocusPopup(FocusModalView, Popup):
    """"""
    def __init__(self, focus_return=None, **kwargs):
        FocusModalView.__init__(self, focus_return=focus_return, **kwargs)


class FocusRelativeLayout(FocusAwareWidget, RelativeLayout):
    """"""
    def __init__(self, **kwargs):
        RelativeLayout.__init__(self, **kwargs)
        FocusAwareWidget.__init__(self, **kwargs)


class FocusScatterLayout(FocusAwareWidget, ScatterLayout):
    """"""
    def __init__(self, **kwargs):
        ScatterLayout.__init__(self, **kwargs)
        FocusAwareWidget.__init__(self, **kwargs)


class FocusStackLayout(FocusAwareWidget, StackLayout):
    """"""
    def __init__(self, **kwargs):
        StackLayout.__init__(self, **kwargs)
        FocusAwareWidget.__init__(self, **kwargs)


class FocusScreenManager(FocusAwareWidget, ScreenManager):
    """"""
    def __init__(self, **kwargs):
        ScreenManager.__init__(self, **kwargs)
        FocusAwareWidget.__init__(self, **kwargs)


    def add_widget(self, screen):
        ScreenManager.add_widget(self, screen)
        if len(self.screens) == 1:
            self.current_screen.focus_first()


    def on_change_screen(self, manager, new_screen):
        for s in self.screens:
            if s is not new_screen and isinstance(s, FocusAwareWidget):
                s.disable_focus()

        if isinstance(new_screen, FocusAwareWidget):
            new_screen.enable_focus()


class FocusScreen(FocusAwareWidget, Screen):
    """"""
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        FocusAwareWidget.__init__(self, **kwargs)

        self.bind(on_enter=self.focus_first)


    def focus_first(self, *args):
        for widg in self.walk():
            if isinstance(widg, FocusWidget):
                widg.focus = True
                break
