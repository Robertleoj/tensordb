import sqlite3
from pathlib import Path
from typing import Type

import tensordb._backend.collections as collections
import tensordb._backend.db as db
from tensordb._backend.sql_types import SQL_TYPE_TO_TYPE
from tensordb._config import CONFIG
from tensordb._utils.naming import check_name_valid
from tensordb._utils.sqlite import get_table_fields
from tensordb.fields import Field


class Backend:
    """The backend for the database.

    For now, stores the database in a sqlite3 database.
    """

    # Where the database is stored
    dir: Path

    __sqlite_db_path: Path
    __connection: sqlite3.Connection

    def __init__(self, dir: Path) -> None:
        """Initialize a new Backend.

        Args:
            dir: The directory where the database is stored.
        """
        self.dir = dir
        self.__sqlite_db_path = self.dir / "db.db"
        self.__connection = sqlite3.connect(self.__sqlite_db_path)
        db.initialize_db(self.__connection)

    def create_collection(self, name, fields: dict[str, Type | Field]) -> None:
        """Create a new collection.

        Args:
            name: The name of the collection.
            fields: Mapping from field name to field type.
        """
        assert check_name_valid(name), f"{name} is not a valid collection name"

        for field_name in fields.keys():
            assert check_name_valid(field_name), f"{field_name} is not a valid field name"

        if "id" in fields:
            raise ValueError("id is a reserved field name")

        cursor = self.__connection.cursor()

        if collections.collection_exists(name, cursor):
            raise ValueError(f"Collection {name} already exists")

        collections.create_collection_table(name, fields, cursor)
        collection_id = collections.insert_collection(name, cursor)
        collections.insert_collection_fields(collection_id, fields, cursor)

        self.__connection.commit()

    def get_collection_fields(self, name: str) -> dict[str, Type | Field]:
        """Get the fields of a collection.

        Args:
            name: The name of the collection.

        Returns:
            fields: Mapping from field name to field type.
        """
        cursor = self.__connection.cursor()
        tensor_fields = collections.get_collection_tensor_fields(name, cursor)

        all_fields = get_table_fields(name, cursor)

        for key, value in all_fields.items():
            all_fields[key] = SQL_TYPE_TO_TYPE[value]

        all_fields.update(tensor_fields)

        return all_fields

    def collection_exists(self, name: str) -> bool:
        """Check if a collection exists.

        Args:
            name: The name of the collection.

        Returns:
            exists: Whether the collection exists.
        """
        cursor = self.__connection.cursor()
        return collections.collection_exists(name, cursor=cursor)

    def get_collection_names(self) -> list[str]:
        """Get the names of all the collections.

        Returns:
            names: The names of all the collections.
        """
        cursor = self.__connection.cursor()

        cursor.execute(
            f"""
            select name from {CONFIG.reserved_table_names.collections}
        """
        )

        return [row[0] for row in cursor.fetchall()]
