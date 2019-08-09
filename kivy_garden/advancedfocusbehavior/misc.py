import kivy
kivy.require('1.11.1')


def focusable_widgets(start):
    """"""
    return (widg for widg in start.walk(loopback=True) if hasattr(widg, 'focus'))


def focus_first(widg):
    """"""
    for w in focusable_widgets(widg):   # TODO: do this in a less weird way
        #breakpoint()
        w.focus = True
        return w

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
