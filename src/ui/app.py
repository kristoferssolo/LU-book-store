import npyscreen as nps

from .forms import AddBookForm, BookForm


class App(nps.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", BookForm, name="Bookstore")
        self.addForm("ADD_BOOK", AddBookForm, name="Add Book")
