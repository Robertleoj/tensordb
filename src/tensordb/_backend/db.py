import sqlite3

from tensordb._config import CONFIG


def initialize_db(connection: sqlite3.Connection) -> None:
    """Initialize the database."""
    cursor = connection.cursor()

    __create_collections_table(cursor)
    __create_collection_tensor_fields_table(cursor)

    connection.commit()


def __create_collections_table(cursor: sqlite3.Cursor) -> None:
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


def __create_collection_tensor_fields_table(cursor: sqlite3.Cursor) -> None:
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
