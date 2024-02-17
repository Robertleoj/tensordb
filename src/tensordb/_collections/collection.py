from typing import Type

from tensordb._backend import Backend
from tensordb._utils.naming import check_name_valid
from tensordb.fields import Field


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
            self.__backend.create_collection(name, fields)
        else:
            assert self.__backend.collection_exists(name), f"Collection {name} does not exist"

        self.__name = name

    @property
    def fields(self) -> dict[str, Type | Field]:
        return self.__backend.get_collection_fields(self.__name)

    @property
    def name(self) -> str:
        """The name of the collection."""
        return self.__name
