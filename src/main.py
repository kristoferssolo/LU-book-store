#!/usr/bin/env python3


from pathlib import Path

from bookstore.inventory import Inventory

from loguru import logger
from ui.app import App

# Set up logging
logger.add(
    Path("logs", "bookstore.log"),
    format="{time} | {level} | {message}",
    level="INFO",
    rotation="1 MB",
    compression="zip",
)


@logger.catch
def main() -> None:
    db_path = Path("db.sqlite3")
    inventory = Inventory(db_path)
    app = App(inventory)
    app.run()


if __name__ == "__main__":
    main()
