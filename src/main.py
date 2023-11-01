#!/usr/bin/env python3

from pathlib import Path

from bookstore.inventory import Inventory
from ui import tui


def main() -> None:
    db_path = Path("db.sqlite3")
    inventory = Inventory(db_path)
    tui.render(inventory)


if __name__ == "__main__":
    main()
