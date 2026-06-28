from datetime import date
from typing import List
from psycopg.rows import class_row

from db.database import DatabaseManager
from model import Book
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
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Book)) as cur:
                    query = """INSERT INTO book(title, author_name, publication_year, genre_id, total_copies) 
                        VALUES(%s, %s, %s, %s, %s) 
                        RETURNING book_id, title, author_name, publication_year, genre_id, total_copies"""
                    result = cur.execute(
                        query, (title, author, publication_year, genre_id, copy_count)
                    ).fetchone()

                    if not result:
                        logger.error(
                            f"Error encountered while creating new record for {title} by {author}!"
                        )
                        raise ValueError("Error encountered on db operation!")
                    return result

    def get_by_id(self, book_id) -> Book:
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Book)) as cur:
                    query = """SELECT book_id, title, author_name, publication_year, genre_id, total_copies
                        FROM book WHERE book_id = %s"""
                    result = cur.execute(query, (book_id,)).fetchone()

                    if not result:
                        logger.error(f"No record found for book_id: {book_id}")
                        raise ValueError("Error encountered on db operation!")
                    return result

    def get_all(self) -> List[Book]:
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Book)) as cur:
                    query = """SELECT book_id, title, author_name, publication_year, genre_id, total_copies
                        FROM book"""
                    result = cur.execute(query).fetchall()

                    if not result:
                        logger.error("No records found!")
                        raise ValueError("Error encountered on db operation!")
                    return result

    def update(
        self, book_id, title, author, publication_year, genre_id, copy_count
    ) -> Book:
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
                                    publication_year, genre_id, total_copies"""
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

    def delete(self, book_id) -> None:
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    query = "DELETE FROM book WHERE book_id = %s"
                    cur.execute(query, (book_id,))

                    if cur.rowcount == 0:
                        logger.error(f"No record found for book_id: {book_id}")
                        raise ValueError("Error encountered on db operation!")
