from pathlib import Path

from tensordb._utils.paths import get_persistent_data_path


def get_database_root_path() -> Path:
    """Returns the root path for auto-located databases.

    # TODO: maybe use a different path if we are in a virtual env
    """
    return get_persistent_data_path() / "databases"


def get_database_path(database_name: str, base_path: Path | None = None) -> Path:
    """Returns the path to the.

    Args:
        database_name: The name of the database
        base_path: The base path for databases
            If None, it will use the default path.
    """
    if base_path is None:
        base_path = get_database_root_path()

    return base_path / database_name
