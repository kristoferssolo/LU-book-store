import urwid


class Table(urwid.ListBox):
    def __init__(self, body):
        super().__init__(body)
