import sqlite3
from pathlib import Path

from .book import Book
from .isbn import ISBN


class Inventory:
    def __init__(self, db_path: Path) -> None:
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            r"""
            CREATE TABLE IF NOT EXISTS Book (
                isbn TEXT PRIMARY KEY NOT NULL,
                title TEXT DEFAULT 'Unknown' NOT NULL,
                author TEXT DEFAULT 'Unknown' NOT NULL ,
                price REAL DEFAULT 0 NOT NULL,
                stock INTEGER DEFAULT 0 NOT NULL
            )
            """
        )

    def save(self) -> None:
        """Save `Inventory` to SQLite database."""
        self.conn.commit()

    def close(self) -> None:
        """Close database connection."""
        self.conn.close()

    def add(self, book: Book) -> None:
        """Add `Book` to the `Inventory`. `Book`s ISBN must be unique."""
        try:
            self.cursor.execute("INSERT INTO Book VALUES (?, ?, ?, ?, ?)", (book.isbn, book.title, book.author, book.price, book.stock))
            self.conn.commit()
            print(f"Book with ISBN: {book.isbn} was saved")
        except sqlite3.InternalError:
            print(f"A book with ISBN {book.isbn} already exists in the database.")

    def delete(self, isbn: ISBN) -> Book | None:
        """Deletes `Book` from `Inventory` by `ISBN` and returns deleted `Book`"""
        deleted_book = self.find_by_isbn(isbn)

        self.cursor.execute("DELETE FROM Book WHERE isbn = ?", (isbn,))
        self.conn.commit()

        return deleted_book

    def find_by_isbn(self, isbn: ISBN) -> Book | None:
        """Looks up `Book` within `Inventory` by book `ISBN` and returns it. Returns `None` if it doesn't exist."""
        self.cursor.execute("SELECT * FROM Book WHERE isbn = ?", (isbn,))
        book = self.cursor.fetchone()
        if not book:
            return None
        return Book(*book)

    def find_by_title(self, title: str) -> list[Book] | None:
        """Looks up `Book`s within `Inventory` by book title and returns them as a `List`. Returns `None` if none were found"""
        self.cursor.execute("SELECT * FROM Book WHERE title = ?", (title,))
        books = self.cursor.fetchall()
        if not books:
            return None
        return [Book(*book) for book in books]

    def find_by_author(self, author: str) -> list[Book] | None:
        """Looks up `Book`s within `Inventory` by book author and returns them as a `List`. Returns `None` if none were found"""
        self.cursor.execute("SELECT * FROM Book WHERE author = ?", (author,))
        books = self.cursor.fetchall()
        if not books:
            return None
        return [Book(*book) for book in books]

    def list_all(self) -> list[Book | None]:
        """Returns `List` of all `Book`s."""
        self.cursor.execute("SELECT * FROM Book")
        books = self.cursor.fetchall()
        return [Book(*book) for book in books]
