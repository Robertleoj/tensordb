from pathlib import Path

from tensordb import Database


def test_basic_queries(tmp_path: Path) -> None:  # noqa: D103
    db = Database("test_db", tmp_path)

    coll = db.collection("test", fields={"field1": int, "field2": str})

    num_tests = 10

    coll.insert([{"field1": i, "field2": f"test{i}"} for i in range(num_tests)])

    result = coll.find().execute()

    assert len(result) == num_tests

    for i, row in enumerate(result):
        assert row["id"] == i + 1, f"Row {i} has the wrong id"
        assert row["field1"] == i, f"Row {i} has the wrong field1"
        assert row["field2"] == f"test{i}", f"Row {i} has the wrong field2"

    test_i = 5
    result = coll.find({"field1": test_i}).execute()
    assert len(result) == 1
    assert result[0]["field1"] == test_i
    assert result[0]["field2"] == f"test{test_i}"
    assert result[0]["id"] == test_i + 1
