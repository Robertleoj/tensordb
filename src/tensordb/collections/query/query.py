from typing import Any

from tensordb.backend import Backend
from tensordb.collections.functions import get_collection_fields
from tensordb.collections.query.build_query import build_query


class Query:
    __collection_name: str
    __conditions: dict | None
    __fields: list[str] | None
    __backend: Backend

    def __init__(self, collection_name: str, query: dict | None, backend: Backend) -> None:
        """Initialize the query.

        Args:
            collection_name: The name of the collection.
            query: The query to execute.
            backend: The backend to use.
        """
        self.__collection_name = collection_name
        self.__conditions = query
        self.__backend = backend
        self.__fields = None

    def select(self, fields: list[str]) -> "Query":
        """Select fields from the collection.

        Args:
            fields: The fields to select.

        Returns:
            The query.
        """
        assert self.__fields is None, "Fields have already been selected"

        self.__fields = fields

        return self

    def execute(self) -> list[dict[str, Any]]:
        """Execute the query.

        Returns:
            The result of the query.
        """
        cursor = self.__backend.cursor()
        collection_fields = get_collection_fields(self.__collection_name, cursor=cursor)

        fields, sql_query, substitutions = build_query(
            collection_name=self.__collection_name,
            query_conditions=self.__conditions,
            fields=self.__fields,
            backend=self.__backend,
            collection_fields=collection_fields,
            cursor=cursor,
        )

        cursor.execute(sql_query, substitutions)

        return [dict(zip(fields, row)) for row in cursor.fetchall()]
