from pathlib import Path

from tensordb import Database


def test_create_database(tmp_path: Path) -> None:  # noqa: D103
    base_path = tmp_path
    db_name = "test_db"

    db = Database(db_name, base_path=base_path)

    assert db.location == base_path / db_name, "The location is not correct"
