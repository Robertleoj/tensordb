import sqlite3
from typing import Any

from tensordb.collections.functions import get_collection_fields


def insert_data(collection_name: str, data: list[dict[str, Any]], cursor: sqlite3.Cursor) -> None:
    """Insert data into the collection.

    Args:
        collection_name: The name of the collection.
        data: The data to insert.
        cursor: The cursor to use to execute the command.
    """
    fields = get_collection_fields(collection_name, cursor)
    fields.pop("id")

    for row in data:
        assert set(row.keys()) == set(fields.keys()), f"Row {row} does not have the correct fields"

        values = [row[field_name] for field_name in fields.keys()]

        cursor.execute(
            f"""
            insert into {collection_name} ({", ".join(fields.keys())})
            values ({", ".join(["?"] * len(fields))})
        """,
            values,
        )
