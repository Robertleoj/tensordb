import sqlite3

from tensordb.config import CONFIG


def create_collections_table(cursor: sqlite3.Cursor) -> None:
    """Create the collections table.

    Args:
        cursor: The cursor to use to execute the command.
    """
    table_name = CONFIG.reserved_table_names.collections

    cursor.execute(
        f"""
        create table if not exists {table_name} (
            id integer primary key,
            name text unique
        )
    """
    )


def create_collection_tensor_fields_table(cursor: sqlite3.Cursor) -> None:
    """Create the collection tensor fields table.

    Args:
        cursor: The cursor to use to execute the command.
    """
    table_name = CONFIG.reserved_table_names.collection_tensor_fields

    cursor.execute(
        f"""
        create table if not exists {table_name} (
            id integer primary key,
            collection_id integer,
            field_name text,
            dtype text,
            shape blob,
            unique(collection_id, field_name)
        )
    """
    )


def get_collection_names(cursor: sqlite3.Cursor) -> list[str]:
    """Get the names of all the collections.

    Args:
        cursor: The cursor to use to execute the command.
    """
    cursor.execute(
        f"""
        select name from {CONFIG.reserved_table_names.collections}
    """
    )

    return [row[0] for row in cursor.fetchall()]
