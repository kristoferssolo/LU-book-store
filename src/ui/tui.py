import urwid
from bookstore.book import Book
from bookstore.inventory import Inventory

from .handlers import exit_on_q

from .widgets.table import Table


def create_row(cells) -> urwid.Columns:
    return urwid.Columns([urwid.Text(str(cell)) for cell in cells])


def create_books_table(books: list[Book]) -> Table:
    header = create_row(Book.fields())
    rows = [create_row(book.field_values()) for book in books]
    return Table(urwid.SimpleListWalker([header] + rows))


def render(inventory: Inventory):
    books_table = create_books_table(inventory.list_all())
    loop = urwid.MainLoop(books_table, unhandled_input=exit_on_q)
    loop.run()
