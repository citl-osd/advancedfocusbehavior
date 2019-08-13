import kivy
kivy.require('1.11.1')

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.stacklayout import StackLayout

from kivy_garden.advancedfocusbehavior.behaviors import FocusAwareWidget


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


class FocusPageLayout(FocusAwareWidget, PageLayout):
    """"""
    def __init__(self, **kwargs):
        PageLayout.__init__(self, **kwargs)
        FocusAwareWidget.__init__(self, **kwargs)


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
