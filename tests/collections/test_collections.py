from pathlib import Path

import pytest
from tensordb import Database
from tensordb.fields import TensorField


def test_get_fields(tmp_path: Path) -> None:  # noqa: D103
    db = Database("test_db", tmp_path)

    collection_name = "test_collection"
    collection_fields = {
        "field1": int,
        "field2": float,
        "field3": str,
        "tensorfield": TensorField(dtype=int, shape=(None, 2)),
    }

    collection = db.collection(collection_name, fields=collection_fields)

    recovered_fields = collection.fields
    recovered_fields_no_id = {key: value for key, value in recovered_fields.items() if key != "id"}

    assert recovered_fields_no_id == collection_fields, "The fields are not correct"

    assert recovered_fields["id"] == int, "The id field should be an int"


def test_make_id_column(tmp_path: Path) -> None:  # noqa: D103
    """Providing an 'id' field shoud raise an error."""
    db = Database("test_db", tmp_path)

    with pytest.raises(ValueError):
        db.collection("test", fields={"id": int})
