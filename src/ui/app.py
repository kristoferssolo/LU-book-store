import customtkinter as ctk
from bookstore.book import Book
from bookstore.inventory import Inventory


class App(ctk.CTk):
    def __init__(self, inventory: Inventory, *args, **kwargs) -> None:
        super(App, self).__init__(*args, **kwargs)
        self.inventory = inventory

        self.geometry("600x400")
        self.title("Bookstore")
        ctk.set_appearance_mode("system")
        self.resizable(width=True, height=True)
        self.data = inventory.list_all()

        self.display_table()
        self.display_add_button()

    def display_table(self) -> None:
        headers = Book.fields()
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self, text=header)
            label.grid(row=0, column=col, padx=10, pady=5)

        widths = [100, 100, 100, 100, 100]
        for row, book in enumerate(self.data, start=1):
            for col, value in enumerate(book):
                entry = ctk.CTkLabel(self, width=widths[col], text=value)
                entry.grid(row=row, column=col, padx=10, pady=5)

    def display_add_button(self) -> None:
        add_book_button = ctk.CTkButton(self, text="Add Book", command=self.add_book)
        add_book_button.grid(row=0, column=5, padx=10, pady=5)

    def search(self) -> None:
        pass

    def run(self) -> None:
        self.mainloop()

    def add_book(self) -> None:
        popup = ctk.CTkToplevel(self)
        popup.title("Add Book")

        entries = []
        for index, value in enumerate(Book.fields()):
            title = ctk.CTkLabel(popup, text=value)
            title.grid(row=index, column=0, padx=10, pady=5)
            entry = ctk.CTkEntry(
                popup,
                width=200,
            )
            entry.grid(row=index, column=1, padx=10, pady=5)
            entries.append(entry)

        def submit():
            values = [entry.get() for entry in entries]
            book = Book(*values)
            self.inventory.add(book)
            popup.destroy()
            self.update()

        submit_button = ctk.CTkButton(popup, text="Submit", command=submit)
        submit_button.grid(row=5, column=0, padx=10, pady=5)

    def update(self):
        self.data = self.inventory.list_all()
        self.display_table()
