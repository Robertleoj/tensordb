from pathlib import Path

from tensordb import Database


def test_query(tmp_path: Path) -> None:  # noqa: D103
    db = Database("test_db", tmp_path)

    coll = db.collection("test", fields={"field1": int, "field2": str})

    coll.insert([{"field1": 1, "field2": "test"}, {"field1": 2, "field2": "test2"}, {"field1": 3, "field2": "test3"}])

    result = coll.find().execute()

    assert len(result) == 3
