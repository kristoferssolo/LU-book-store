import urwid


def exit_on_q(key):
    """Define a function to handle exit when the `q` key is pressed"""
    if key in ("q", "Q"):
        raise urwid.ExitMainLoop()
