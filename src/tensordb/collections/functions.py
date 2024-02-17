import sqlite3
from typing import Type

import msgpack
import numpy as np

from tensordb.backend import Backend
from tensordb.config import CONFIG
from tensordb.fields import Field, TensorField
from tensordb.utils.naming import check_name_valid
from tensordb.utils.sqlite import SQL_TYPE_TO_TYPE, TYPE_TO_SQL_TYPE, get_table_fields


def get_collection_fields(name: str, cursor: sqlite3.Cursor) -> dict[str, Type | Field]:
    """Get the fields of a collection.

    Args:
        name: The name of the collection.
        cursor: The cursor to use to execute the command.

    Returns:
        fields: Mapping from field name to field type.
    """
    tensor_fields = get_collection_tensor_fields(name, cursor)

    all_fields = get_table_fields(name, cursor)

    for key, value in all_fields.items():
        all_fields[key] = SQL_TYPE_TO_TYPE[value]

    all_fields.update(tensor_fields)

    return all_fields


def collection_exists(name: str, cursor: sqlite3.Cursor) -> bool:
    """Check if a collection exists.

    Args:
        name: The name of the collection.
        cursor: The cursor to use to execute the command.

    Returns:
        exists: Whether the collection exists.
    """
    cursor.execute(
        f"""
        select * from {CONFIG.reserved_table_names.collections}
        where name = ?
    """,
        (name,),
    )

    result = cursor.fetchall()
    return len(result) > 0


def create_collection(name, fields: dict[str, Type | Field], backend: Backend) -> None:
    """Create a new collection.

    Args:
        name: The name of the collection.
        fields: Mapping from field name to field type.
        backend: The backend to use.
    """
    assert check_name_valid(name), f"{name} is not a valid collection name"

    for field_name in fields.keys():
        assert check_name_valid(field_name), f"{field_name} is not a valid field name"

    if "id" in fields:
        raise ValueError("id is a reserved field name")

    cursor = backend.cursor()

    if collection_exists(name, cursor):
        raise ValueError(f"Collection {name} already exists")

    create_collection_table(name, fields, cursor)
    collection_id = insert_collection(name, cursor)
    insert_collection_fields(collection_id, fields, cursor)

    backend.commit()


def create_collection_table(name: str, fields: dict[str, Type | Field], cursor: sqlite3.Cursor) -> None:
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


def insert_collection(name: str, cursor: sqlite3.Cursor | None = None) -> int:
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


def insert_collection_fields(
    collection_id: int,
    fields: dict[str, Type | Field],
    cursor: sqlite3.Cursor,
) -> None:
    """Insert the fields of a collection into the collection_tensor_fields table.

    Args:
        collection_id: The id of the collection.
        fields: Mapping from field name to field type.
        cursor: The cursor to use to execute the command.
    """
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


def get_collection_tensor_fields(collection_name: str, cursor: sqlite3.Cursor) -> dict[str, TensorField]:
    """Get the tensor fields of a collection.

    Args:
        collection_name: The name of the collection.
        cursor: The cursor to use to execute the command.

    Returns:
        tensor_fields: Mapping from field name to tensor field.
    """
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
