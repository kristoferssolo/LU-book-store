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
        ctk.set_default_color_theme("dark-blue")
        self.resizable(width=True, height=True)
        self.data = inventory.list_all()

        self.display()

    def display(self) -> None:
        """Display the main application interface."""
        self.populate_table()
        self.display_search()
        self.display_add_button()

    def populate_table(self) -> None:
        """Populate the table in the main window with book data."""
        headers = Book.fields()

        for col, header in enumerate(headers):  # Create header labels for each column
            label = ctk.CTkLabel(self, text=header, width=self.WIDTH)
            label.grid(row=0, column=col, padx=self.PADX, pady=self.PADY)

        widths = (110, 250, 150, 50, 50)

        for row, book in enumerate(self.data, start=1):  # Iterate through list of books
            if book:
                for col, value in enumerate(book):  # Iterate through book data
                    entry = ctk.CTkEntry(self, width=widths[col])
                    entry.insert(ctk.END, value)
                    entry.configure(state="readonly")
                    entry.grid(row=row, column=col, padx=self.PADX, pady=self.PADY)

                # Add edit button for each book entry
                self.button(self, text="Edit", command=lambda book=book: self.edit_book(book), width=0.5 * self.WIDTH, row=row, col=5)

    def edit_book(self, book: Book):
        """Open a book editing menu."""
        self.book_menu(title_text="Edit Book", book=book)

    def display_search(self) -> None:
        """Display a search entry field in the main window."""
        search_entry = ctk.CTkEntry(self, width=2 * self.WIDTH)
        search_entry.grid(row=0, column=6, padx=self.PADX, pady=self.PADY)

        def search(event=None) -> None:
            """Search for b books when <Enter> key ir pressed in the search entry field."""
            value = search_entry.get()
            if value == "":
                self.refresh()
            else:
                data = []
                # Search for books with matching ISBN in the inventory.
                isbn = self.inventory.find_by_isbn(value)
                if isbn:
                    data.append(isbn)

                # Search for books with matching title in the inventory.
                titles = self.inventory.find_by_title(value)
                if titles:
                    data += titles

                # Search for books with matching author in the inventory.
                authors = self.inventory.find_by_author(value)
                if authors:
                    data += authors

                self.refresh(data)

        # Bind the search function to the <Enter> key press
        search_entry.bind("<Return>", command=search)

    def display_add_button(self) -> None:
        """Display a button for adding a new book in the main window."""
        self.button(self, text="Add Book", command=self.add_book, width=2 * self.WIDTH, row=2, col=6)

    def run(self) -> None:
        """Run the main loop."""
        self.mainloop()

    def add_book(self) -> None:
        """Open a menu for adding a new book."""
        self.book_menu(title_text="Add Book")

    def book_menu(self, /, *, title_text: str = "", book: Book = None):
        """Display a book editing/adding menu."""
        # Create a new popup window.

        popup = ctk.CTkToplevel(self)
        popup.title(title_text)

        edit = True if book else False

        entries: list[ctk.CTkEntry] = []

        for index, field in enumerate(Book.fields()):  # Iterate through book fields and create labels and entry fields for each
            title = ctk.CTkLabel(popup, text=field)
            title.grid(row=index, column=0, padx=self.PADX, pady=self.PADY)
            entry = ctk.CTkEntry(popup, width=2 * self.WIDTH)

            # Set the default value in the entry field based on the book's data
            value = book.get(field, "") if book else ""
            entry.insert(ctk.END, str(value))

            # If editing a book and the field is ISBN, set the entry field to read-only.
            if field == "ISBN" and edit:
                entry.configure(state="readonly")

            entry.grid(row=index, column=1, padx=self.PADX, pady=self.PADY)
            entries.append(entry)

        def save() -> None:
            """Save the changes or addition made in the book menu."""
            values = [entry.get() for entry in entries]
            book = Book(*values)
            if edit:
                self.inventory.edit(book)
            else:
                self.inventory.add(book)
            popup.destroy()
            self.refresh()

        def delete() -> None:
            """Delete the book from the inventory."""
            self.inventory.delete(book.isbn)
            popup.destroy()
            self.refresh()

        def cancel() -> None:
            """Close the book menu."""
            popup.destroy()

        self.button(popup, text="Save", command=save, width=2 * self.WIDTH, row=5, col=1)
        self.button(popup, text="Cancel", command=cancel, width=2 * self.WIDTH, row=6, col=1)

        if edit:
            self.button(popup, text="Delete Book", command=delete, width=self.WIDTH, row=5, col=0, fg_color="#9b0d0d", hover_color="#720101")

    def button(
        self,
        root,
        /,
        *,
        text: str,
        command,
        width: int | float,
        row: int,
        col: int,
        padx: int = PADX,
        pady: int = PADY,
        text_color: str | None = None,
        fg_color: str | None = None,
        hover_color: str | None = None,
    ) -> None:
        """Create a button in a `root` window."""
        button = ctk.CTkButton(root, text=text, command=command, width=width, text_color=text_color, fg_color=fg_color, hover_color=hover_color)
        button.grid(row=row, column=col, padx=padx, pady=pady)

    def refresh(self, data=None) -> None:
        """Update the table with new data or reset it."""
        self.clear_table()
        self.data = data if data else self.inventory.list_all()
        self.display()

    def clear_table(self) -> None:
        """Clear the table in the main window."""
        for widget in self.grid_slaves():
            if isinstance(widget, ctk.CTkEntry) or isinstance(widget, ctk.CTkButton):
                widget.destroy()
