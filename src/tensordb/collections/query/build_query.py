import sqlite3
from typing import Any

from tensordb.backend import Backend


def build_query(
    collection_name: str,
    query_conditions: dict | None,
    fields: list[str] | None,
    backend: Backend,
    collection_fields: dict[str, Any],
    cursor: sqlite3.Cursor | None = None,
) -> tuple[list[str], str, tuple[Any]]:
    """Build a query to execute.

    Args:
        collection_name: The name of the collection.
        query_conditions: The query conditions.
            If None, all rows will be selected.
        fields: The fields to select.
            If None, all fields will be selected.
        backend: The backend to use.
        collection_fields: The fields of the collection.
        cursor: The cursor to use to execute the command.
            If None, a new cursor will be created.


    """
    sql_query = f"""
        select
            {{fields}}
        from
            {collection_name}
        where
            {{conditions}}
    """
    fmt_params = {}

    if cursor is None:
        cursor = backend.cursor()

    if fields is None:
        fields = list(collection_fields.keys())
    else:
        assert all(field in collection_fields for field in fields), "Invalid field selected"

    fmt_params["fields"] = ", ".join(fields)

    substitutions = []
    if query_conditions is None:
        fmt_params["conditions"] = "1"
    else:
        fields_to_query = []
        field_query_values = []
        for field, value in query_conditions.items():
            assert field in collection_fields, "Invalid field in query"
            fields_to_query.append(field)
            field_query_values.append(value)

        conditions = " and ".join(f"{field} = ?" for field in fields_to_query)

        fmt_params["conditions"] = conditions

        substitutions.extend(field_query_values)

    sql_query = sql_query.format_map(fmt_params)

    return fields, sql_query, tuple(substitutions)
