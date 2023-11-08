import sqlite3
from pathlib import Path

from loguru import logger

from .book import Book
from .isbn import ISBN


class Inventory:
    @logger.catch
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

    @logger.catch
    def save(self) -> None:
        """Save `Inventory` to SQLite database."""
        self.conn.commit()

    @logger.catch
    def close(self) -> None:
        """Close database connection."""
        self.conn.close()

    @logger.catch
    def add(self, *books: Book) -> None:
        """Add `Book` to the `Inventory`. `Book`s ISBN must be unique."""
        for book in books:
            try:
                self.cursor.execute("INSERT INTO Book VALUES (?, ?, ?, ?, ?)", (book.isbn, book.title, book.author, book.price, book.stock))
                self.save()
                logger.info(f"Create: {book}")
            except sqlite3.InternalError as e:
                logger.error(f"A book with ISBN {book.isbn} already exists in the database.\t{e}")

    @logger.catch
    def edit(self, book: Book) -> None:
        """Edit `Book`."""
        try:
            self.cursor.execute(
                "UPDATE Book SET title = ?, author = ?, price = ?, stock = ? WHERE isbn = ?", (book.title, book.author, book.price, book.stock, book.isbn)
            )
            self.save()
            logger.info(f"Update: {book}")
        except sqlite3.InternalError as e:
            logger.error(f"Something went wrong.\t{e}")

    @logger.catch
    def delete(self, isbn: ISBN) -> Book | None:
        """Deletes `Book` from `Inventory` by `ISBN` and returns deleted `Book`"""
        deleted_book = self.find_by_isbn(isbn)

        self.cursor.execute("DELETE FROM Book WHERE isbn = ?", (isbn,))
        self.save()
        logger.info(f"Delete: {deleted_book}")

        return deleted_book

    @logger.catch
    def find_by_isbn(self, isbn: ISBN) -> Book | None:
        """Looks up `Book` within `Inventory` by book `ISBN` and returns it. Returns `None` if it doesn't exist."""
        self.cursor.execute("SELECT * FROM Book WHERE isbn = ?", (isbn,))
        book = self.cursor.fetchone()
        if not book:
            return None
        return Book(*book)

    @logger.catch
    def find_by_title(self, title: str) -> list[Book] | None:
        """Looks up `Book`s within `Inventory` by book title and returns them as a `List`. Returns `None` if none were found"""
        self.cursor.execute("SELECT * FROM Book WHERE title LIKE ?", (f"%{title}%",))
        books = self.cursor.fetchall()
        if not books:
            return None
        return [Book(*book) for book in books]

    @logger.catch
    def find_by_author(self, author: str) -> list[Book] | None:
        """Looks up `Book`s within `Inventory` by book author and returns them as a `List`. Returns `None` if none were found"""
        self.cursor.execute("SELECT * FROM Book WHERE author LIKE ?", (f"%{author}%",))
        books = self.cursor.fetchall()
        if not books:
            return None
        return [Book(*book) for book in books]

    @logger.catch
    def list_all(self) -> list[Book | None]:
        """Returns `List` of all `Book`s."""
        self.cursor.execute("SELECT * FROM Book")
        books = self.cursor.fetchall()
        return [Book(*book) for book in books]
