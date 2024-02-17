from typing import Any, Type

from tensordb.collections.functions import collection_exists, create_collection, get_collection_fields, insert_data
from tensordb.fields import Field
from tensordb.type_defs import Backend
from tensordb.utils.naming import check_name_valid


class Collection:
    """A collection of data."""

    __name: str
    __backend: Backend

    def __init__(
        self,
        name: str,
        backend: Backend,
        fields: dict[str, Type | Field] | None,
    ) -> None:
        """Initialize the collection.

        Args:
            name: The name of the collection.
            backend: The backend to use
            fields: Mapping from field name to field type.
        """
        assert check_name_valid(name), f"{name} is not a valid name"

        self.__backend = backend

        if fields is not None:
            create_collection(name, fields, self.__backend)
        else:
            assert collection_exists(name, self.__backend.cursor()), f"Collection {name} does not exist"

        self.__name = name

    @property
    def fields(self) -> dict[str, Type | Field]:
        """The fields of the collection."""
        return get_collection_fields(self.__name, self.__backend.cursor())

    @property
    def name(self) -> str:
        """The name of the collection."""
        return self.__name

    def insert(self, data: dict[str, Any] | list[dict[str, Any]]) -> None:
        """Insert data into the collection.

        Args:
            data: The data to insert.
        """
        if isinstance(data, dict):
            data = [data]

        cursor = self.__backend.cursor()
        insert_data(self.__name, data, cursor)
        self.__backend.commit()

    def query(self, query: dict) -> list[dict[str, Any]]:
        """Query the collection.

        Args:
            query: The query to execute.

        Returns:
            The results of the query.
        """
        pass
