import csv
from pathlib import Path

from .book import Book
from .isbn import ISBN


class Inventory:
    def __init__(self, books: list[Book] | None) -> None:
        self.books: dict[ISBN, Book] = {book.isbn: book for book in books} if books else {}

    def read_from_file(self, path: Path) -> None:
        """Read `Inventory` from `path` csv file."""
        with open(path, mode="r") as file:
            reader = csv.reader(file)

            next(reader, None)  # Skip header

            for title, author, isbn, price, stock in reader:
                book = Book(title, author, isbn, price, stock)
                self.add(book)

    def save_to_file(self, path: Path) -> None:
        """Save `Inventory` to `path` csv file."""
        with open(path, mode="w") as file:
            writer = csv.writer(file)

            writer.writerow(["Title", "Auther", "ISBN", "Price", "Stock"])

            for book in self.books.values():
                writer.writerow([book.title, book.author, book.isbn, book.price, book.stock])

    def add(self, book: Book) -> None:
        """Add `Book` to the `Inventory`. `Book`s ISBN must be unique."""
        if book.isbn in self.books:
            raise BaseException(f"Book with this ISBN: {book.isbn} already exists!")  # TODO: create custom exception

        self.books[book.isbn] = book

    def delete(self, isbn: ISBN) -> Book | None:
        """Deletes `Book` from `Inventory` by `isbn` and returns deleted `Book`"""
        return self.books.pop(isbn, None)

    def find_by_isbn(self, isbn: ISBN) -> Book | None:
        """Looks up `Book` within `Inventory` by book `ISBN` and returns it. Returns `None` if it doesn't exist."""
        if isbn not in self.books.keys():
            return None
        return self.books.get(isbn)

    def find_by_title(self, title: str) -> list[Book] | None:
        """Looks up `Book`s within `Inventory` by book title and returns them as a `List`. Returns `None` if none were found"""
        found_books = []
        for book in self.books.values():
            if book.title.lower() == title.strip().lower():
                found_books.append(book)

        if found_books:
            return found_books
        return None

    def find_by_author(self, author: str) -> list[Book] | None:
        """Looks up `Book`s within `Inventory` by book author and returns them as a `List`. Returns `None` if none were found"""

        found_books = []
        for book in self.books.values():
            if book.author.lower() == author.strip().lower():
                found_books.append(book)

        if found_books:
            return found_books
        return None

    def list_all(self) -> list[Book]:
        """Returns `List` of all `Book`s."""
        return list(self.books.values())
