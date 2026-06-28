from typing import List

from psycopg.rows import class_row

from db.database import DatabaseManager
from logger import logger
from model import Genre


class GenreDAO:
    def __init__(self):
        self._db_manager = DatabaseManager()

    def create(self, genre_name: str) -> Genre:
        """
        Insert a new genre record into the database.

        :param genre_name: The name of the genre to create.
        :type genre_name: str
        :returns: The newly created Genre object with its assigned ID and name.
        :rtype: Genre
        :raises ValueError: If the insert operation returns no result.
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Genre)) as cur:
                    query = "INSERT INTO genre(genre_name) VALUES (%s) RETURNING genre_id, genre_name"
                    result = cur.execute(query, (genre_name,)).fetchone()

                    if not result:
                        logger.error(
                            f"Error encountered while creating new record for {genre_name}!"
                        )
                        raise ValueError("Error encountered on db operation!")
                    return result

    def get_by_id(self, genre_id) -> Genre:
        """
        Retrieve a single genre record by its primary key.

        :param genre_id: The primary key of the genre to fetch.
        :returns: The Genre object matching the given ID.
        :rtype: Genre
        :raises ValueError: If no genre record is found for the given ID.
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Genre)) as cur:
                    query = "SELECT genre_id, genre_name FROM genre WHERE genre_id = %s"
                    result = cur.execute(query, (genre_id,)).fetchone()

                    if not result:
                        logger.error(f"No record found for genre_id: {genre_id}!")
                        raise ValueError("Error encountered on db operation!")
                    return result

    def get_all(self) -> List[Genre]:
        """
        Retrieve all genre records from the database.

        :returns: A list of all Genre objects stored in the genre table.
        :rtype: List[Genre]
        :raises ValueError: If no genre records are found or the table is empty.
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Genre)) as cur:
                    query = "SELECT genre_id, genre_name FROM genre"
                    result = cur.execute(query).fetchall()

                    if not result:
                        logger.error("Error encountered while fetching genre records!")
                        raise ValueError("Error encountered on db operation!")
                    return result

    def update(self, genre_id, genre_name) -> Genre:
        """
        Update the name of an existing genre record.

        :param genre_id: The primary key of the genre to update.
        :param genre_name: The new name to assign to the genre.
        :type genre_name: str
        :returns: The updated Genre object reflecting the new name.
        :rtype: Genre
        :raises ValueError: If no genre record is found for the given ID.
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Genre)) as cur:
                    query = """UPDATE genre SET genre_name = %s 
                        WHERE genre_id = %s RETURNING genre_id, genre_name"""
                    result = cur.execute(query, (genre_name, genre_id)).fetchone()

                    if not result:
                        logger.error(
                            f"Error encountered while updating genre_name: {genre_name} for genre_id: {genre_id}!"
                        )
                        raise ValueError("Error encountered on db operation!")
                    return result

    def delete(self, genre_id) -> None:
        """
        Delete a genre record from the database by its primary key.

        :param genre_id: The primary key of the genre to delete.
        :returns: None
        :raises ValueError: If no genre record is found for the given ID.
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    query = "DELETE FROM genre WHERE genre_id = %s"
                    cur.execute(query, (genre_id,))

                    if cur.rowcount == 0:
                        logger.error(f"No record found for genre_id: {genre_id}")
                        raise ValueError("Error encountered on db operation!")
