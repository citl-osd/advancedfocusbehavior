import kivy
kivy.require('1.11.1')

from itertools import chain


def focusable_widgets(start):
    """"""
    # If this is called from an on_parent event, the widget will have a parent,
    # but the parent won't have the widget listed as a child yet
    if not start.parent or start in start.parent.children:
        return (widg for widg in start.walk(loopback=True) if hasattr(widg, 'focus'))

    return (widg for widg in chain(start.walk(loopback=True),
                start.parent.walk(loopback=True)) if hasattr(widg, 'focus'))


def focus_first(widg):
    """"""
    try:
        w = next(focusable_widgets(widg))
        w.focus = True
        return w

    except StopIteration:
        # No focusable widgets
        return None


def find_first_focused(widg, start_at_next=False):
    """"""
    for w in focusable_widgets(widg):
        if w is widg and start_at_next:
            continue

        if w.focus:
            return w

    return None
