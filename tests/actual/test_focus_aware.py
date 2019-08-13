import kivy
kivy.require('1.11.1')

from common import run_in_app

from kivy_garden.advancedfocusbehavior import FocusBoxLayout, FocusButton, FocusWidget

def test_get_focus_upon_entering():
    # If there are no focused widgets, the first focusable widget should receive focus
    container = FocusBoxLayout()
    widg = FocusWidget()
    assert not widg.focus
    container.add_widget(widg)
    assert widg.focus


def test_multiple_focusable_adds():
    container = FocusBoxLayout()
    first = FocusWidget()
    second = FocusWidget()
    container.add_widget(first)
    container.add_widget(second)
    assert first.focus
    assert not second.focus


def test_remove_focused_widget():
    container = FocusBoxLayout()
    first = FocusWidget()
    second = FocusWidget()
    container.add_widget(first)
    container.add_widget(second)

    container.remove_widget(first)
    assert second.focus
