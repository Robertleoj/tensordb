from pathlib import Path


def get_persistent_data_path() -> Path:
    """Returns the path to the persistent data folder.

    This is where autocreated resources will be stored
    """
    return Path.home() / ".tensordb"


def get_package_root() -> Path:
    """Get the root path of the package."""
    # Your current file's path
    current_path = Path(__file__).resolve()

    # Keep moving up until you hit your package root
    while not (current_path / "pyproject.toml").exists():
        current_path = current_path.parent

    return current_path
