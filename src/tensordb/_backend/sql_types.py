TYPE_TO_SQL_TYPE = {
    int: "INTEGER",
    float: "REAL",
    str: "TEXT",
}

SQL_TYPE_TO_TYPE = {value: key for key, value in TYPE_TO_SQL_TYPE.items()}
