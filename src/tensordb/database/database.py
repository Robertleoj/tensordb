import logging
from pathlib import Path
from typing import Type

from tensordb.backend import Backend, get_backend
from tensordb.collections import Collection
from tensordb.config import CONFIG
from tensordb.database.functions import (
    create_collection_tensor_fields_table,
    create_collections_table,
    get_collection_names,
)
from tensordb.database.paths import get_database_path
from tensordb.fields import Field
from tensordb.utils.naming import check_name_valid

logger = logging.getLogger(__name__)

COLLECTIONS_TABLE_NAME = CONFIG.reserved_table_names.collections


class Database:
    # The directory where the database is stored
    __db_name: str
    __backend: Backend

    def __init__(self, db_name: str, base_path: Path | None = None) -> None:
        """Create a new TorchDB database.

        Args:
            db_name: The name of the database
            base_path: The base path where you want to store TorchDB databases
                If None, it will use the default path.
        """
        if not check_name_valid(db_name):
            raise ValueError(f"{db_name} is not a valid name")

        db_dir = get_database_path(db_name, base_path)
        self.__db_name = db_name

        if not db_dir.exists():
            db_dir.mkdir(parents=True)
            logger.info(f"Creating new database at {db_dir}")
        else:
            logger.info(f"Loading existing database at {db_dir}")

        self.__backend = get_backend(db_dir)

        cursor = self.__backend.cursor()

        create_collections_table(cursor)
        create_collection_tensor_fields_table(cursor)

        self.__backend.commit()

    def collection(self, name: str, fields: dict[str, Type | Field] | None = None) -> Collection:
        """Get an existing collection, or create a new one.

        Args:
            name: The name of the collection
            fields: Mapping from field name to field type.
                If None, will attempt to get an existing collection.
                If not None, another collection with the same name cannot
                already exist.

        Returns:
            collection: The collection with the given name.
        """
        assert check_name_valid(name), f"{name} is not a valid name"

        return Collection(name=name, backend=self.__backend, fields=fields)

    def collections(self) -> list[str]:
        """Return a list of all the collections in the database."""
        cursor = self.__backend.cursor()
        return get_collection_names(cursor)

    def __repr__(self) -> str:
        """Returns a string representation of the database.

        TODO: Add the collections
        """
        return f"Database(name={self.__db_name})"

    @property
    def location(self) -> Path:
        """Returns the location of the database."""
        return self.__backend.dir
