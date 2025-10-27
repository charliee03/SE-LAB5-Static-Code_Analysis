"""Small inventory management helpers used in Lab 5 static analysis.

Provides functions to add/remove items, persist to JSON, and report stock
levels. This module also contains a simple `main` demo runner.
"""

import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

stock_data = {}


def add_item(item=None, qty=0, logs=None):
    """Add item to stock with validation.

    Parameters
    - item: str name of the item
    - qty: int quantity to add (can be zero or negative for removal)
    - logs: optional list to append timestamped messages
    """
    if logs is None:
        logs = []

    if not isinstance(item, str) or not isinstance(qty, int):
        logging.warning("Invalid input types for item or quantity.")
        return

    if not item:
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d units of %s.", qty, item)


def remove_item(item, qty):
    """Remove quantity from stock safely.

    Only handles missing items and type errors explicitly.
    """
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
            logging.info("Removed all of %s from stock.", item)
    except KeyError:
        logging.warning("Item '%s' not found in inventory.", item)
    except TypeError as e:
        logging.error("Unexpected type error while removing item: %s", e)


def get_qty(item):
    """Return current quantity of an item."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Load stock data from JSON file.

    Loads JSON and updates the module-level `stock_data` dict in-place so
    callers don't need to use the global statement.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        logging.info("Inventory loaded successfully.")
    except FileNotFoundError:
        logging.warning("%s not found. Starting with empty inventory.", file)
        data = {}
    # update the existing dict instead of rebinding the name
    stock_data.clear()
    stock_data.update(data)


def save_data(file="inventory.json"):
    """Save stock data to JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, indent=4)
    logging.info("Inventory saved successfully.")


def print_data():
    """Display all items in stock."""
    print("\nItems Report")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold=5):
    """Return list of low-stock items."""
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """Simple demo runner used when executing the module directly."""
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")  # Invalid input — now safely ignored
    remove_item("apple", 3)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()


if __name__ == "__main__":
    main()
