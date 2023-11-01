import urwid
from bookstore.book import Book
from bookstore.inventory import Inventory

from .handlers import exit_on_q
from .widgets.table import Table


FOCUS_STYLE = urwid.AttrMap("default", "dark red", "standout")
UNFOCUS_STYLE = urwid.AttrMap("default", "default", "standout")


def create_books_table(books: list[Book]) -> Table:
    header = urwid.Columns([urwid.Text(header) for header in Book.fields()])
    header = urwid.AttrMap(header, "header", focus_map=FOCUS_STYLE)

    rows = [header]

    for book in books:
        row = urwid.Columns([urwid.Text(str(value)) for value in book.field_values()])
        rows.append(urwid.AttrMap(row, "body", focus_map=FOCUS_STYLE))

    walker = urwid.SimpleListWalker(rows)
    books_table = Table(walker)
    return books_table


def render(inventory: Inventory):
    books_table = create_books_table(inventory.list_all())
    loop = urwid.MainLoop(books_table, unhandled_input=exit_on_q)
    loop.run()
