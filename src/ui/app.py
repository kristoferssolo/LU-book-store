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


    def run(self) -> None:
        self.mainloop()

