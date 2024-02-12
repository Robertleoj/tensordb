import logging
import sqlite3
from pathlib import Path

from tensordb._config import Config
from tensordb._database.paths import get_database_path

logger = logging.getLogger(__name__)

COLLECTIONS_TABLE_NAME = Config.config.reserved_table_names.collections


class Database:
    def __init__(self, db_name: str, base_path: Path | None = None) -> None:
        """Create a new TorchDB database.

        Args:
            db_name: The name of the database
            base_path: The base path where you want to store TorchDB databases
                If None, it will use the default path.
        """
        self.__db_dir = get_database_path(db_name, base_path)
        self.__sqlite_db_path = self.__db_dir / "db.db"
        self.__db_name = db_name

        if not self.__db_dir.exists():
            self.__db_dir_path.mkdir(parents=True)
            logger.info(f"Creating new database at {self.__db_dir}")
        else:
            logger.info(f"Loading existing database at {self.__db_dir}")

        self.__initialize_db()

    def __repr__(self) -> str:
        """Returns a string representation of the database.

        TODO: Add the collections
        """
        return f"Database(name={self.__db_name})"

    def __initialize_db(self) -> None:
        """Initialize a new database."""
        self.__connection = sqlite3.connect(self.__sqlite_db_path)
        cursor = self.__connection.cursor()

        cursor.execute(
            """
            create table if not exists ? (
                id integer primary key,
                name text
            )
        """,
            (COLLECTIONS_TABLE_NAME,),
        )

        cursor.commit()

    @property
    def location(self) -> Path:
        """Returns the location of the database."""
        return self.__db_dir
