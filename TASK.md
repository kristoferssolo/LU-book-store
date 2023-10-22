# Task

<!-- toc -->

- [Data structure](#data-structure)
- [Functionality](#functionality)
  * [Add book](#add-book)
  * [Search by ISBN](#search-by-isbn)
  * [Search by title or author](#search-by-title-or-author)
  * [Book list](#book-list)
  * [Delete book](#delete-book)
- [User interface](#user-interface)
- [Submission](#submission)

<!-- tocstop -->

## Data structure

- [ ] The inventory list is stored as a Python dictionary.
- [ ] The original list of books can be *hard coded* into the program to avoid having to re-enter the data each time.
- [ ] At least the following information is stored for each book: `title`, `author`, `ISBN`, `price` and `quantity in stock`.
- [ ] Information for each book is stored in a separate dictionary
- [ ] The keys of the inventory dictionary are the `ISBN` codes and its values are the dictionaries containing the information about the book.

## Functionality

### Add book

- [ ] The user should be given the possibility to add a new book to the inventory.
- [ ] When adding a book, make sure that its ISBN number is unique. If such an ISBN number already exists in the list, display an error message.

### Search by ISBN

- [ ] Users should be allowed to search for a book by its ISBN number.
- [ ] If the book was found, display information about it.
- [ ] If the book was not found, display an error message.

### Search by title or author

- [ ] Allow users to search for a book by name in its title or author field. The result is a list of books that match the search criteria.

### Book list

- [ ] Display a list of all books, showing the following information for each book: `title`, `author`, `ISBN`, `quantity in stock`.

### Delete book

- [ ] Delete a book with a given ISBN number from the list.
- [ ] To inform the user that the book was successfully deleted or that the ISBN number was not found.

## User interface

For a score of 8, it is sufficient to implement a simple textual interface.

For a higher score, develop a program with a graphical user interface (using Python libraries such as `Tkinter`, `PyQt` or `PySide`).
You can also use the `rich` library, which allows you to create an *advanced* text format interface.

## Submission

Submit an archive with the source code of a Python program that implements the requested functionality.
The program code must be properly documented (with comments and meaningful variable names).

If external libraries are used, include in the archive a `requirements.txt` file containing the names and version numbers of these libraries.
