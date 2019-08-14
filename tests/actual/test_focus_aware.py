import kivy
kivy.require('1.11.1')

from kivy.uix.label import Label

from common import run_in_app

from kivy_garden.advancedfocusbehavior import FocusBoxLayout, FocusButton

def test_get_focus_upon_entering():
    # If there are no focused widgets, the first focusable widget should receive focus
    container = FocusBoxLayout()
    widg = FocusButton()
    container.add_widget(widg)
    assert widg.focus
    assert container.focus_target is widg


def test_multiple_focusable_adds():
    container = FocusBoxLayout()
    first = FocusButton()
    second = FocusButton()
    container.add_widget(first)
    container.add_widget(second)
    assert first.focus
    assert not second.focus


def test_remove_focused_widget():
    container = FocusBoxLayout()
    first = FocusButton()
    second = FocusButton()
    container.add_widget(first)
    container.add_widget(second)

    container.remove_widget(first)
    assert second.focus
    assert container.focus_target is second


def test_defocus_all():
    container = FocusBoxLayout()
    widg = FocusButton()
    container.add_widget(widg)

    container.remove_widget(widg)
    assert not widg.focus
    assert container.focus_target is None


def test_add_tree_focus():
    outer = FocusBoxLayout()
    inner = FocusBoxLayout()
    outer.add_widget(Label())
    outer.add_widget(Label())

    assert outer.focus_target is None

    c = FocusButton()
    inner.add_widget(c)
    outer.add_widget(inner)

    assert c.focus
    assert outer.focus_target is c


def test_focus_override():
    container = FocusBoxLayout()
    a, b, c = [FocusButton() for _ in range(3)]
    for btn in (a, b, c):
        container.add_widget(btn)

    assert a.focus
    assert container.focus_target is a
    print('a is focused')

    c.focus = True
    print('c is focused')

    assert c.focus
    assert container.focus_target is c
