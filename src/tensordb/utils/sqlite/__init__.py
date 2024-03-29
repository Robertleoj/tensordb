import sqlite3

TYPE_TO_SQL_TYPE = {
    int: "INTEGER",
    float: "REAL",
    str: "TEXT",
}

SQL_TYPE_TO_TYPE = {value: key for key, value in TYPE_TO_SQL_TYPE.items()}


def get_table_fields(table_name: str, cursor: sqlite3.Cursor) -> dict[str, str]:
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
