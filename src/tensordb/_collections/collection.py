from typing import Type

from tensordb._backend import Backend
from tensordb._utils.naming import check_name_valid
from tensordb.fields import Field


class Collection:
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

        if fields is None:
            # Get the collection
            backend.create_collection(name, fields)

        else:
            # Create a new collection
            pass
