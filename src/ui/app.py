import customtkinter as ctk
from bookstore.book import Book
from bookstore.inventory import Inventory


class App(ctk.CTk):
    WIDTH = 100
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
                edit_button = ctk.CTkButton(self, text="Edit", command=lambda: self.edit_book(book), width=0.5 * self.WIDTH)
                edit_button.grid(row=row, column=5, padx=self.PADX, pady=self.PADY)

    def edit_book(self, book: Book):
        self.book_menu(title_text="Edit Book", button_text="Save", book=book)

    def display_search(self) -> None:
        search_entry = ctk.CTkEntry(self, width=2 * self.WIDTH)
        search_entry.grid(row=0, column=6, padx=self.PADX, pady=self.PADY)

        def search(event=None) -> None:
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
        add_book_button = ctk.CTkButton(self, text="Add Book", command=self.add_book, width=2 * self.WIDTH)
        add_book_button.grid(row=2, column=6, padx=self.PADX, pady=self.PADY)

    def run(self) -> None:
        self.mainloop()

    def add_book(self) -> None:
        self.book_menu(title_text="Add Book", button_text="Submit")

    def book_menu(self, /, *, title_text: str = "", button_text: str = "", book: Book = None):
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

        def submit():
            values = [entry.get() for entry in entries]
            book = Book(*values)
            if edit:
                self.inventory.edit(book)
            else:
                self.inventory.add(book)
            popup.destroy()
            self.update()

        submit_button = ctk.CTkButton(popup, text=button_text, command=submit)
        submit_button.grid(row=5, column=0, padx=self.PADX, pady=self.PADY)

    def update(self, data=None) -> None:
        self.clear_table()
        if data:
            self.data = data
        else:
            self.data = self.inventory.list_all()
        self.populate_table()

    def clear_table(self):
        for widget in self.grid_slaves():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()
