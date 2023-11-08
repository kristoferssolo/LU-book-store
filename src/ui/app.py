import customtkinter as ctk
from bookstore.book import Book
from bookstore.inventory import Inventory


class App(ctk.CTk):
    WIDTH = 110
    PADX = 10
    PADY = 5

    def __init__(self, inventory: Inventory, *args, **kwargs) -> None:
        super(App, self).__init__(*args, **kwargs)
        self.inventory = inventory

        self.geometry("960x540")
        self.title("Bookstore")
        ctk.set_appearance_mode("system")
        self.resizable(width=True, height=True)
        self.data = inventory.list_all()

        self.populate_table()
        self.display_search()
        self.display_add_button()

    def populate_table(self) -> None:
        """Populate the table in the main window with book data."""
        headers = Book.fields()
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self, text=header, width=self.WIDTH)
            label.grid(row=0, column=col, padx=self.PADX, pady=self.PADY)

        for row, book in enumerate(self.data, start=1):
            if book:
                for col, value in enumerate(book):
                    entry = ctk.CTkEntry(self, width=self.WIDTH)
                    entry.insert(ctk.END, value)
                    entry.configure(state="readonly")
                    entry.grid(row=row, column=col, padx=self.PADX, pady=self.PADY)
                edit_button = ctk.CTkButton(self, text="Edit", command=lambda book=book: self.edit_book(book), width=0.5 * self.WIDTH)
                edit_button.grid(row=row, column=5, padx=self.PADX, pady=self.PADY)

    def edit_book(self, book: Book):
        """Open a book editing menu."""
        self.book_menu(title_text="Edit Book", button_text="Save", book=book)

    def display_search(self) -> None:
        """Display a search entry field in the main window."""
        search_entry = ctk.CTkEntry(self, width=2 * self.WIDTH)
        search_entry.grid(row=0, column=6, padx=self.PADX, pady=self.PADY)

        def search(event=None) -> None:
            """Search for b books when <Enter> key ir pressed in the search entry field."""
            value = search_entry.get()
            if value == "":
                self.update()
            else:
                data = []
                isbn = self.inventory.find_by_isbn(value)
                if isbn:
                    data.append(isbn)

                title = self.inventory.find_by_title(value)
                if title:
                    data += title

                author = self.inventory.find_by_author(value)
                if author:
                    data += author

                self.update(data)

        search_entry.bind("<Return>", command=search)

    def display_add_button(self) -> None:
        """Display a button for adding a new book in the main window."""
        self.button(self, text="Add Book", command=self.add_book, width=2 * self.WIDTH, row=2, col=6)

    def run(self) -> None:
        """Run the main loop."""
        self.mainloop()

    def add_book(self) -> None:
        """Open a menu for adding a new book."""
        self.book_menu(title_text="Add Book", button_text="Submit")

    def book_menu(self, /, *, title_text: str = "", button_text: str = "", book: Book = None):
        """Display a book editing/adding menu."""
        popup = ctk.CTkToplevel(self)
        popup.title(title_text)
        edit = True if book else False

        entries: list[ctk.CTkEntry] = []

        for index, field in enumerate(Book.fields()):
            title = ctk.CTkLabel(popup, text=field)
            title.grid(row=index, column=0, padx=self.PADX, pady=self.PADY)
            entry = ctk.CTkEntry(popup, width=2 * self.WIDTH)
            value = book.get(field, "") if book else ""
            entry.insert(ctk.END, str(value))
            if field == "ISBN" and edit:
                entry.configure(state="readonly")
            entry.grid(row=index, column=1, padx=self.PADX, pady=self.PADY)
            entries.append(entry)

        def submit() -> None:
            """Submit the changes or addition made in the book menu."""
            values = [entry.get() for entry in entries]
            book = Book(*values)
            if edit:
                self.inventory.edit(book)
            else:
                self.inventory.add(book)
            popup.destroy()
            self.update()

        def delete() -> None:
            """Delete the book from the inventory."""
            self.inventory.delete(book.isbn)
            popup.destroy()
            self.update()

        def cancel() -> None:
            """Close the book menu."""
            popup.destroy()

        self.button(popup, text=button_text, command=submit, width=2 * self.WIDTH, row=5, col=1)
        self.button(popup, text="Cancel", command=cancel, width=2 * self.WIDTH, row=6, col=1)

        if edit:
            self.button(popup, text="Delete Book", command=delete, width=self.WIDTH, row=5, col=0)

    def button(self, root, /, *, text: str, command, width: int, row: int, col: int, padx: int = PADX, pady: int = PADY) -> None:
        """Create a button in a `root` window."""
        button = ctk.CTkButton(root, text=text, command=command, width=width)
        button.grid(row=row, column=col, padx=padx, pady=pady)

    def update(self, data=None) -> None:
        """Update the table with new data or reset it."""
        self.clear_table()
        if data:
            self.data = data
        else:
            self.data = self.inventory.list_all()
        self.populate_table()

    def clear_table(self) -> None:
        """Cleat the table in the main window."""
        for widget in self.grid_slaves():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()
