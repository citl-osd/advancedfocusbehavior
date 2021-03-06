import kivy
kivy.require('1.11.1')

from kivy.uix.label import Label

from common import run_in_app

from kivy_garden.advancedfocusbehavior import FocusBoxLayout, FocusButton, link_focus

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

    c.focus = True

    assert c.focus
    assert container.focus_target is c


def test_disable_some_focus():
    outer = FocusBoxLayout()
    inner = FocusBoxLayout()
    a = FocusButton()
    b = FocusButton()

    outer.add_widget(a)
    outer.add_widget(inner)
    inner.add_widget(b)

    b.focus = True
    assert outer.focus_target is b

    inner.set_focus_enabled(False)

    assert a.focus


def test_disable_all_focus():
    container = FocusBoxLayout()
    a, b, c = [FocusButton() for _ in range(3)]

    for btn in (a, b, c):
        container.add_widget(btn)

    container.set_focus_enabled(False)
    assert container.focus_target is None


def test_reenable_focus():
    container = FocusBoxLayout()
    btn = FocusButton()
    container.add_widget(btn)
    container.set_focus_enabled(False)
    assert not btn.focus

    container.set_focus_enabled(True)
    assert btn.focus


def test_link_focus_no_loopback():
    focusables = [FocusButton() for _ in range(10)]
    link_focus(focusables)
    for i, widget in enumerate(focusables):
        if i > 0:
            assert widget.focus_previous is focusables[i - 1]
        if i < len(focusables) - 1:
            assert widget.focus_next is focusables[i + 1]

    assert focusables[0].focus_previous is None
    assert focusables[-1].focus_next is None


def test_link_focus_loopback():
    focusables = [FocusButton() for _ in range(10)]
    link_focus(focusables, loopback=True)
    for i, widget in enumerate(focusables):
        assert widget.focus_previous is focusables[(i - 1) % len(focusables)]
        assert widget.focus_next is focusables[(i + 1) % len(focusables)]


def test_link_empty():
    focusables = []
    link_focus(focusables)
    assert focusables == []


def test_link_one():
    btn = FocusButton()
    focusables = [btn]
    link_focus(focusables)
    assert btn.focus_previous is None
    assert btn.focus_next is None


def test_link_one_loopback():
    btn = FocusButton()
    focusables = [btn]
    link_focus(focusables, loopback=True)
    assert btn.focus_previous is None
    assert btn.focus_next is None
