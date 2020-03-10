"""
Advanced Focus Behavior
============

Defines all widgets and behaviors for Advanced Focus Behavior.
"""

__version__ = '0.1.0.dev0'

from pathlib import Path
import sys

focus_dest = str(Path(__file__).parents[1].resolve())
if focus_dest not in sys.path:
    sys.path.append(focus_dest)

from kivy_garden.advancedfocusbehavior.behaviors import *
from kivy_garden.advancedfocusbehavior.focusable import *
from kivy_garden.advancedfocusbehavior.focus_aware import *
