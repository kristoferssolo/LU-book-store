import npyscreen as nps
from bookstore.book import Book

from .utils import INVENTORY
from .widget import BookGrid


class BookForm(nps.FormBaseNew):
    def create(self):
        self.grid = self.add_widget(BookGrid, columns=5, select_whole_line=True, col_titles=Book.fields())
        self.grid.values = [book.values() for book in INVENTORY.list_all()]


class AddBookForm(nps.ActionForm):
    def create(self):
        self.isbn = self.add(nps.TitleText, name="ISBN:")
        self.title = self.add(nps.TitleText, name="Title:")
        self.author = self.add(nps.TitleText, name="Author:")
        self.price = self.add(nps.TitleText, name="Price:")
        self.stock = self.add(nps.TitleText, name="Stock:")

    def on_ok(self):
        book = Book(self.isbn.value, self.title.value, self.author.value, self.price.value, self.stock.value)
        INVENTORY.add(book)
