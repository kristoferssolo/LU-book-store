from pathlib import Path

from bookstore.inventory import Inventory

INVENTORY = Inventory(Path("db.sqlite3"))
