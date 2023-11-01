import customtkinter as ctk
from bookstore.book import Book
from bookstore.inventory import Inventory


class UI:
    def __init__(self, inventory: Inventory) -> None:
        self.inventory = inventory
        self.theme()
        self.root = ctk.CTk()
        self.root.geometry("650x400")
        self.frame = ctk.CTkFrame(self.root)

    def render(self) -> None:
        self._create_gui()
        self.root.mainloop()

    def theme(self, mode: str = "dark", color: str = "dark-blue") -> None:
        ctk.set_appearance_mode(mode)
        ctk.set_default_color_theme(color)

    def _create_gui(self) -> None:
        self._show()

        label = ctk.CTkLabel(self.frame, text="LU Bookstore")
        label.pack(pady=12, padx=10)

        button = ctk.CTkButton(self.frame, text="New book", command=self._add_book)
        button.pack(pady=12, padx=10)

    def _list_books(self) -> None:
        pass

    def _add_book(self) -> None:
        self._hide()
        self._show()

        placeholders = ("ISBN", "Title", "Author", "Price", "Stock")
        self.entries: list[ctk.CTkEntry] = []

        for placeholder in placeholders:
            entry = ctk.CTkEntry(self.frame, placeholder_text=placeholder)
            entry.pack(pady=12, padx=10)
            self.entries.append(entry)

        button = ctk.CTkButton(self.frame, text="Save", command=self._save_book)
        button.pack(pady=12, padx=10)

    def _save_book(self) -> None:
        entry_values = [entry.get() for entry in self.entries]
        if entry_values[0]:  # ISBN must be a value
            new_book = Book(*entry_values)
            self.inventory.add(new_book)

            for entry in self.entries:
                entry.destroy()
            self.entries = []
            self._show()

    def _hide(self) -> None:
        self.frame.pack_forget()

    def _show(self) -> None:
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)
