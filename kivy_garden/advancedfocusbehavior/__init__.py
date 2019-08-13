"""
Demo flower
============

Defines the Kivy garden :class:`FlowerLabel` class which is the widget provided
by the demo flower.
"""

#__all__ = ('FlowerLabel', )

__version__ = '0.1.0.dev0'

from pathlib import Path
import sys

focus_dest = str(Path(__file__).parents[1].resolve())
if focus_dest not in sys.path:
    sys.path.append(focus_dest)

from kivy_garden.advancedfocusbehavior.behaviors import *
from kivy_garden.advancedfocusbehavior.focusable import *
from kivy_garden.advancedfocusbehavior.focus_aware import *
