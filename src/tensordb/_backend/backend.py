import sqlite3
from pathlib import Path
from typing import Type

from tensordb._config import CONFIG
from tensordb._utils.naming import check_name_valid
from tensordb.fields import Field


class Backend:
    """The backend for the database.

    For now, stores the database in a sqlite3 database.
    """

    # Where the database is stored
    dir: Path

    __sqlite_db_path: Path
    __connection: sqlite3.Connection

    def __init__(self, dir: Path):
        self.dir = dir
        self.__sqlite_db_path = self.__db_dir / "db.db"
        self.__connection = sqlite3.connect(self.__sqlite_db_path)
        self.__initialize_db()

    def __initialize_db(self) -> None:
        """Initialize the database."""
        cursor = self.__connection.cursor()

        self.__create_collections_table(cursor)
        self.__create_collection_tensor_fields_table(cursor)

        self.__connection.commit()

    def __create_collections_table(self, cursor: sqlite3.Cursor) -> None:
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

    def __create_collection_tensor_fields_table(self, cursor: sqlite3.Cursor) -> None:
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
                dtype text,
                shape blob
            )
        """
        )

    def create_collection(self, name, fields: dict[str, Type | Field]) -> None:
        """Create a new collection.

        Args:
            name: The name of the collection.
            fields: Mapping from field name to field type.
        """
        assert check_name_valid(name), f"{name} is not a valid collection name"

        cursor = self.__connection.cursor()

        if self.__collection_exists(name, cursor):
            raise ValueError(f"Collection {name} already exists")

        self.__insert_collection(name, cursor)

    def __insert_collection_fields(
        self, collection_id: int, fields: dict[str, Type | Field], cursor: sqlite3.Cursor | None = None
    ) -> None:
        """Insert the fields of a collection into the collection_tensor_fields table.

        Args:
            collection_id: The id of the collection.
            fields: Mapping from field name to field type.
            cursor: The cursor to use to execute the command.
                If None, will create a new cursor.
        """
        if cursor is None:
            cursor = self.__connection.cursor()

        # TODO: Implement this

    def __insert_collection(self, name: str, cursor: sqlite3.Cursor | None = None) -> int:
        """Insert a collection into the collections table.

        Args:
            name: The name of the collection.
            cursor: The cursor to use to execute the command.
                If None, will create a new cursor.

        Returns:
            id: The id of the collection.
        """
        cursor.execute(
            f"""
            insert into {CONFIG.reserved_table_names.collections} (name)
            values (?)
        """,
            (name,),
        )

        cursor.execute(
            f"""
            select id from {CONFIG.reserved_table_names.collections}
            where name = ?
        """,
            (name,),
        )

        return cursor.fetchone()[0]

    def __collection_exists(self, name: str, cursor: sqlite3.Cursor | None = None) -> bool:
        """Check if a collection exists.

        Args:
            name: The name of the collection.
            cursor: The cursor to use to execute the command.
                If None, will create a new cursor.

        Returns:
            exists: Whether the collection exists.
        """
        if cursor is None:
            cursor = self.__connection.cursor()

        cursor.execute(
            f"""
            select * from {CONFIG.reserved_table_names.collections}
            where name = ?
        """,
            (name,),
        )

        return cursor.fetchall() is not None
