from pathlib import Path

import pytest
from tensordb._backend import Backend


@pytest.mark.disk_io
def test_backend_collection_exists(tmp_path: Path) -> None:  # noqa: D103
    backend = Backend(tmp_path)

    collection_name = "test_collection"

    assert not backend.collection_exists(collection_name), "Collection should not exist"

    backend.create_collection(collection_name, fields={"field1": int})

    assert backend.collection_exists(collection_name), "Collection should exist"

    assert not backend.collection_exists("non_existent_collection"), "Collection should not exist"
