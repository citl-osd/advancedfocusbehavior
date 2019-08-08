import kivy
kivy.require('1.11.1')


def find_first_focused(widg):
    """"""
    for w in widg.walk(loopback=True):
        if hasattr(w, 'focus') and w.focus:
            return w

    return None
