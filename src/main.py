#!/usr/bin/env python3


from pathlib import Path

from bookstore.inventory import Inventory
from ui.app import App


def main() -> None:
    db_path = Path("db.sqlite3")
    inventory = Inventory(db_path)
    app = App(inventory)
    app.run()


if __name__ == "__main__":
    main()
