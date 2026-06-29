from typing import List, Optional
from psycopg.rows import class_row

from db.database import DatabaseManager
from models.book import Book
from logger import logger


class BookDAO:
    def __init__(self, db_manager: DatabaseManager):
        self._db_manager = db_manager

    def create(
        self,
        title: str,
        author: str,
        publication_year: str,
        genre_id: int,
        copy_count: int,
    ) -> Book:
        """
        Insert a new book record into the database.

        :param title: The title of the book.
        :type title: str
        :param author: The full name of the book's author.
        :type author: str
        :param publication_year: The year the book was published.
        :type publication_year: str
        :param genre_id: The foreign key referencing the book's genre.
        :type genre_id: int
        :param copy_count: The total number of copies available.
        :type copy_count: int
        :returns: The newly created Book object with its assigned ID and all fields.
        :rtype: Book
        :raises ValueError: If the insert operation returns no result.
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Book)) as cur:
                    query = """INSERT INTO book(title, author_name, publication_year, genre_id, total_copies, available_copies) 
                        VALUES(%s, %s, %s, %s, %s, %s) 
                        RETURNING book_id, title, author_name, publication_year, genre_id, total_copies, available_copies"""
                    result = cur.execute(
                        query,
                        (
                            title,
                            author,
                            publication_year,
                            genre_id,
                            copy_count,
                            copy_count,
                        ),
                    ).fetchone()

                    if not result:
                        logger.error(
                            f"Error encountered while creating new record for {title} by {author}!"
                        )
                        raise ValueError("Error encountered on db operation!")
                    return result

    def get_by_id(self, book_id) -> Optional[Book]:
        """
        Retrieve a single book record by its primary key.

        :param book_id: The primary key of the book to fetch.
        :returns: The Book object matching the given ID.
        :rtype: Book | None
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Book)) as cur:
                    query = """SELECT book_id, title, author_name, publication_year, genre_id, total_copies, available_copies
                        FROM book WHERE book_id = %s"""
                    result = cur.execute(query, (book_id,)).fetchone()
                    return result

    def get_all(self) -> List[Book]:
        """
        Retrieve all book records from the database.

        :returns: A list of all Book objects stored in the book table.
        :rtype: List[Book]
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Book)) as cur:
                    query = """SELECT book_id, title, author_name, publication_year, genre_id, total_copies, available_copies
                        FROM book"""
                    result = cur.execute(query).fetchall()
                    return result

    def update(
        self, book_id, title, author, publication_year, genre_id, copy_count
    ) -> Book:
        """
        Update all fields of an existing book record.

        :param book_id: The primary key of the book to update.
        :param title: The new title to assign to the book.
        :type title: str
        :param author: The new author name to assign to the book.
        :type author: str
        :param publication_year: The new publication year to assign to the book.
        :type publication_year: str
        :param genre_id: The new genre foreign key to assign to the book.
        :type genre_id: int
        :param copy_count: The new total copy count to assign to the book.
        :type copy_count: int
        :returns: The updated Book object reflecting all new field values.
        :rtype: Book
        :raises ValueError: If no book record is found for the given ID.
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Book)) as cur:
                    query = """UPDATE book 
                                SET title = %s,
                                    author_name = %s,
                                    publication_year = %s,
                                    genre_id = %s,
                                    total_copies = %s
                                WHERE book_id = %s 
                                RETURNING book_id, title, author_name, 
                                    publication_year, genre_id, total_copies, available_copies"""
                    result = cur.execute(
                        query,
                        (
                            title,
                            author,
                            publication_year,
                            genre_id,
                            copy_count,
                            book_id,
                        ),
                    ).fetchone()

                    if not result:
                        logger.error(
                            f"Error encountered while updating book_id: {book_id}!"
                        )
                        raise ValueError("Error encountered on db operation!")
                    return result

    def update_available_copies(self, book_id: int, available_copies: int) -> Book:
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Book)) as cur:
                    query = """UPDATE book 
                                SET available_copies = %s
                                WHERE book_id = %s 
                                RETURNING book_id, title, author_name, 
                                    publication_year, genre_id, total_copies, available_copies"""
                    result = cur.execute(
                        query,
                        (
                            available_copies,
                            book_id,
                        ),
                    ).fetchone()

                    if not result:
                        logger.error(
                            f"Error encountered while updating book_id: {book_id}!"
                        )
                        raise ValueError("Error encountered on db operation!")

                    logger.info(f"Updated available copies for book_id: {book_id}...")
                    return result

    def delete(self, book_id) -> None:
        """
        Delete a book record from the database by its primary key.

        Unlike a soft delete, this permanently removes the row. A ValueError is
        raised if the given ID does not match any existing record, detected via
        checking the cursor's rowcount after execution.

        :param book_id: The primary key of the book to delete.
        :returns: None
        :raises ValueError: If no book record is found for the given ID.
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    query = "DELETE FROM book WHERE book_id = %s"
                    cur.execute(query, (book_id,))

                    if cur.rowcount == 0:
                        logger.error(f"No record found for book_id: {book_id}")
                        raise ValueError("Error encountered on db operation!")

    def get_by_genre_id(self, genre_id) -> List[Book]:
        """
        Retrieve all book records belonging to a specific genre.

        Unlike other read methods, an empty result is not treated as an error,
        as having no books under a given genre is a valid state.

        :param genre_id: The foreign key of the genre to filter books by.
        :returns: A list of Book objects matching the given genre, or an empty list if none exist.
        :rtype: List[Book]
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Book)) as cur:
                    query = """SELECT book_id, title, author_name, publication_year, genre_id, total_copies, available_copies
                        FROM book WHERE genre_id = %s"""
                    result = cur.execute(query, (genre_id,)).fetchall()
                    return result
