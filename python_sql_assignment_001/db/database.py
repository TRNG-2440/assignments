import os

from dotenv import load_dotenv
import psycopg
from psycopg.sql import SQL
from contextlib import contextmanager
from typing import Optional

from logger import logger

load_dotenv()


class DatabaseManager:
    _instance: Optional["DatabaseManager"] = None
    _conn: Optional[psycopg.Connection] = None
    _db_url = os.getenv("CONN_STR")
    _initialized = False

    def __new__(cls):
        """Standard Singleton pattern implementation using __new__."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if type(self)._initialized:
            return

        self._init_script = os.getenv("INIT_TABLES_SCRIPT")
        if not self._init_script:
            raise ValueError("Database init script not specified!")

        with self.get_connection() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    with open(self._init_script, "r", encoding="utf-8") as f:
                        sql_script = f.read()
                        cur.execute(SQL(sql_script))  # type: ignore

        type(self)._initialized = True

    def _get_persistent_connection(self) -> psycopg.Connection:
        """Returns the single persistent connection, creating it or reconnecting if necessary."""
        # Check if connection doesn't exist or has been closed
        if self._conn is None or self._conn.closed:
            try:
                logger.info("Opening a new persistent database connection.")
                if not self._db_url:
                    raise ValueError(
                        "Database URL must be provided for initial instantiation."
                    )
                self._conn = psycopg.connect(self._db_url)
            except psycopg.Error as e:
                logger.error(f"Error establishing database connection: {e}")
                raise RuntimeError(f"Database error: {e}") from e
        return self._conn

    @contextmanager
    def get_connection(self):
        """Context manager yielding the single, shared connection."""
        try:
            yield self._get_persistent_connection()
        except psycopg.Error as e:
            logger.error(f"Database operation error: {e}")
            raise RuntimeError(f"Database error: {e}") from e

    def close_all(self):
        """Explicitly close the persistent connection when the application shuts down."""
        if self._conn and not self._conn.closed:
            self._conn.close()
            logger.info("Persistent database connection closed.")
