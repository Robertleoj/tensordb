from pathlib import Path

import numpy as np
from tensordb import Database
from tensordb.fields import TensorField


def test_create_database(tmp_path: Path) -> None:  # noqa: D103
    base_path = tmp_path
    db_name = "test_db"

    db = Database(db_name, base_path=base_path)

    assert db.location == base_path / db_name, "The location is not correct"


def test_database_collection(tmp_path: Path) -> None:  # noqa: D103
    """Test that creating a collection works as expected."""
    base_path = tmp_path
    db_name = "test_db"

    db = Database(db_name, base_path=base_path)

    collection_name = "test_collection"

    fields = {"field1": int, "field2": float, "field3": TensorField(dtype=np.int32, shape=(None, 2))}

    collection = db.collection(collection_name, fields=fields)

    assert collection.name == collection_name, "The collection name is not correct"

    collection = db.collection(collection_name)
