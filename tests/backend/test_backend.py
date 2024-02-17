from pathlib import Path

import numpy as np
import pytest
from tensordb._backend import Backend
from tensordb.fields import TensorField


@pytest.mark.disk_io
def test_backend_collection_exists(tmp_path: Path) -> None:  # noqa: D103
    backend = Backend(tmp_path)

    collection_name = "test_collection"

    assert not backend.collection_exists(collection_name), "Collection should not exist"

    backend.create_collection(collection_name, fields={"field1": int})

    assert backend.collection_exists(collection_name), "Collection should exist"

    assert not backend.collection_exists("non_existent_collection"), "Collection should not exist"


@pytest.mark.disk_io
def test_backend_collection_fields(tmp_path: Path) -> None:  # noqa: D103
    backend = Backend(tmp_path)

    collection_name = "test_collection"
    fields = {"field1": int, "field2": float, "field3": int, "field4": TensorField(dtype=np.int32, shape=(None, 2))}

    backend.create_collection(collection_name, fields=fields)

    fields = backend.get_collection_fields(collection_name)

    assert fields == fields, "The fields are not correct"
