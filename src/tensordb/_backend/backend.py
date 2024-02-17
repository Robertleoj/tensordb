import sqlite3
from pathlib import Path
from typing import Type

import msgpack
import numpy as np

from tensordb._backend.sql_types import SQL_TYPE_TO_TYPE, TYPE_TO_SQL_TYPE
from tensordb._config import CONFIG
from tensordb._utils.naming import check_name_valid
from tensordb.fields import Field, TensorField


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
                field_name text,
                dtype text,
                shape blob,
                unique(collection_id, field_name)
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

        for field_name in fields.keys():
            assert check_name_valid(field_name), f"{field_name} is not a valid field name"

        if "id" in fields:
            raise ValueError("id is a reserved field name")

        cursor = self.__connection.cursor()

        if self.__collection_exists(name, cursor):
            raise ValueError(f"Collection {name} already exists")

        self.__create_collection_table(name, fields, cursor)
        collection_id = self.__insert_collection(name, cursor)
        self.__insert_collection_fields(collection_id, fields, cursor)

        self.__connection.commit()

    def get_collection_fields(self, name: str) -> dict[str, Type | Field]:
        """Get the fields of a collection.

        Args:
            name: The name of the collection.

        Returns:
            fields: Mapping from field name to field type.
        """
        cursor = self.__connection.cursor()
        tensor_fields = self.__get_collection_tensor_fields(name, cursor)
        print(tensor_fields)

        all_fields = self.__get_table_fields(name, cursor)

        for key, value in all_fields.items():
            all_fields[key] = SQL_TYPE_TO_TYPE[value]

        all_fields.update(tensor_fields)

        return all_fields

    def __get_table_fields(self, table_name: str, cursor: sqlite3.Cursor) -> dict[str, str]:
        """Get the fields of a table.

        Args:
            table_name: The name of the table.
            cursor: The cursor to use to execute the command.
        """
        cursor.execute(
            f"""
            pragma table_info({table_name})
        """
        )

        fields = {}
        for row in cursor.fetchall():
            field_name = row[1]
            field_type = row[2]
            fields[field_name] = field_type

        return fields

    def __get_collection_tensor_fields(self, collection_name: str, cursor: sqlite3.Cursor) -> dict[str, TensorField]:
        cursor.execute(
            f"""
            select
                field_name,
                dtype,
                shape
            from
                {CONFIG.reserved_table_names.collection_tensor_fields}
            where collection_id = (
                select id from {CONFIG.reserved_table_names.collections}
                where name = ?
            )
        """,
            (collection_name,),
        )

        tensor_fields = {}
        for field_name, dtype, shape in cursor.fetchall():
            tensor_fields[field_name] = TensorField(dtype=np.dtype(dtype), shape=tuple(msgpack.unpackb(shape)))

        return tensor_fields

    def __create_collection_table(self, name: str, fields: dict[str, Type | Field], cursor: sqlite3.Cursor) -> None:
        """Create the table for the collection.

        Args:
            name: The name of the collection.
            fields: Mapping from field name to field type.
            cursor: The cursor to use to execute the command.
        """
        query_template = f"""
            create table if not exists {name} (
                {{field_list}}
            )
        """

        query_field_list = [
            "id integer primary key",
        ]

        for field_name, field_type in fields.items():
            if isinstance(field_type, TensorField):
                query_field_list.append(f"{field_name} text")
            else:
                assert field_type in TYPE_TO_SQL_TYPE, f"Unsupported type: {field_type}"
                sql_type = TYPE_TO_SQL_TYPE[field_type]
                query_field_list.append(f"{field_name} {sql_type}")

        query = query_template.format(field_list=",\n".join(query_field_list))

        cursor.execute(query)

    def collection_exists(self, name: str) -> bool:
        """Check if a collection exists.

        Args:
            name: The name of the collection.

        Returns:
            exists: Whether the collection exists.
        """
        return self.__collection_exists(name)

    def __insert_collection_fields(
        self,
        collection_id: int,
        fields: dict[str, Type | Field],
        cursor: sqlite3.Cursor | None = None,
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

        table_name = CONFIG.reserved_table_names.collection_tensor_fields
        insert_template = f"""
            insert into {table_name} (collection_id, field_name, dtype, shape)
            values
            (?, ?, ?, ?)
        """

        for field_name, field_type in fields.items():
            if isinstance(field_type, TensorField):
                cursor.execute(
                    insert_template,
                    (collection_id, field_name, np.dtype(field_type.dtype).name, msgpack.packb(field_type.shape)),
                )

        self.__connection.commit()

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

        result = cursor.fetchall()
        return len(result) > 0

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
