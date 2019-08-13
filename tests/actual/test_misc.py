import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

from common import run_in_app
from kivy_garden.advancedfocusbehavior import FocusButton, FocusWidget, focusable_widgets,\
                                                focus_first, find_first_focused


def widgets_to_text(widgets):
    return ''.join([b.text for b in widgets])


def test_iterate_focusables():
    upper = BoxLayout()
    lower = BoxLayout()

    a, b, c, d, e = [FocusButton() for _ in range(5)]

    for btn, text in zip((a, b, c, d, e), 'abcde'):
        btn.text = text

    upper.add_widget(a)
    upper.add_widget(lower)
    lower.add_widget(b)
    lower.add_widget(c)
    upper.add_widget(d)
    upper.add_widget(e)

    walk = list(focusable_widgets(c))

    # make sure only FocusButtons were extracted
    for widg in walk:
        assert hasattr(widg, 'text')

    # Check order
    text = widgets_to_text(walk)
    assert text == 'cdeab'


def test_iter_no_focusables():
    root = BoxLayout()
    for _ in range(5):
        root.add_widget(BoxLayout())

    assert not list(focusable_widgets(root))


def test_iter_not_in_tree():    # Simulate iterate during on_parent
    row = BoxLayout()
    a, b, c = [FocusButton() for _ in range(3)]

    for btn, text in zip((a, b, c), 'abc'):
        btn.text = text
        row.add_widget(btn)

    d = FocusButton(text='d')
    d.parent = row

    child_walk = widgets_to_text(focusable_widgets(d))
    parent_walk = widgets_to_text(focusable_widgets(row))

    assert child_walk == 'dabc'
    assert parent_walk == 'abc'


def test_find_focus():
    # When focused widget is deep-ish in the widget tree
    layer_1, layer_2, layer_3 = [BoxLayout() for _ in range(3)]
    a, b, c, d, e, f, g, h = [FocusWidget() for _ in range(8)]

    for widg, label in zip((a, b, c, d, e, f, g, h), 'abcdefgh'):
        print(f'{label}: {widg}')

    for widg in (a, b, c):
        layer_1.add_widget(widg)

    for widg in (d, e, f):
        layer_2.add_widget(widg)

    for widg in (g, h):
        layer_3.add_widget(widg)

    layer_1.add_widget(layer_2)
    layer_2.add_widget(layer_3)

    h.focus = True
    for widg, label in zip((a, b, c, d, e, f, g, h), 'abcdefgh'):
        print(f'{label}: {widg.focus}')

    assert find_first_focused(layer_1) is h


def test_find_focus_skip_first():
    row = BoxLayout()
    a, b, c = [FocusWidget() for _ in range(3)]

    for widg in (a, b, c):
        row.add_widget(widg)

    a.focus = True
    assert find_first_focused(a, start_at_next=True) is None


def test_get_focus_upon_entering():
    # If there are no focused widgets, the first focusable widget should receive focus
    container = BoxLayout()
    widg = FocusWidget()
    assert not widg.focus
    container.add_widget(widg)
    assert widg.focus


def test_multiple_focusable_adds():
    container = BoxLayout()
    first = FocusWidget()
    second = FocusWidget()
    container.add_widget(first)
    container.add_widget(second)
    assert first.focus
    assert not second.focus


def test_remove_focused_widget():
    container = BoxLayout()
    first = FocusWidget()
    second = FocusWidget()
    container.add_widget(first)
    container.add_widget(second)

    container.remove_widget(first)
    assert second.focus
