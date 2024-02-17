"""Useful types."""

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Backend:
    """Data class that holds the backend information.

    Attributes:
        dir: The directory where the database is stored.
        sqlite_db_path: The path to the sqlite database.
        connection: The connection to the sqlite database.
    """

    dir: Path
    sqlite_db_path: Path
    connection: sqlite3.Connection

    def cursor(self) -> sqlite3.Cursor:
        """Returns a cursor to the database."""
        return self.connection.cursor()

    def commit(self) -> None:
        """Commits the current transaction."""
        self.connection.commit()


def get_backend(dir: Path) -> Backend:
    """Return a backend for the given directory.

    Args:
        dir: The directory where the database is stored.
    """
    sqlite_db_path = dir / "db.db"

    connection = sqlite3.connect(sqlite_db_path)

    return Backend(dir=dir, sqlite_db_path=sqlite_db_path, connection=connection)
