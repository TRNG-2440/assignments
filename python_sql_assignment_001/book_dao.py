import psycopg
from psycopg.rows import dict_row
from typing import Optional

from db_util import get_conn_string
from dao import BookRecord


class BookDAO:
    def __init__(self):
        self.conn_string = get_conn_string()

    def _map_row(self, row) -> BookRecord:
        return BookRecord(
            book_id=row["book_id"],
            title=row["title"],
            author_name=row["author_name"],
            publication_year=row["publication_year"],
            genre_id=row["genre_id"],
            copy_count=row["copy_count"]
        )

    def create(
        self,
        title: str,
        author_name: str,
        publication_year: int,
        genre_id: int,
        copy_count: int
    ) -> BookRecord:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    INSERT INTO library.books (
                        title,
                        author_name,
                        publication_year,
                        genre_id,
                        copy_count
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING book_id, title, author_name, publication_year, genre_id, copy_count
                """, (
                    title,
                    author_name,
                    publication_year,
                    genre_id,
                    copy_count
                ))
                row = cursor.fetchone()
                return self._map_row(row)

    def get_by_id(self, book_id: int) -> Optional[BookRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    SELECT book_id, title, author_name, publication_year, genre_id, copy_count
                    FROM library.books
                    WHERE book_id = %s
                """, (book_id,))
                row = cursor.fetchone()
                return self._map_row(row) if row else None

    def get_all(self) -> list[BookRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    SELECT book_id, title, author_name, publication_year, genre_id, copy_count
                    FROM library.books
                    ORDER BY book_id
                """)
                rows = cursor.fetchall()
                return [self._map_row(row) for row in rows]

    def update(
        self,
        book_id: int,
        title: str,
        author_name: str,
        publication_year: int,
        genre_id: int,
        copy_count: int
    ) -> Optional[BookRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    UPDATE library.books
                    SET title = %s,
                        author_name = %s,
                        publication_year = %s,
                        genre_id = %s,
                        copy_count = %s
                    WHERE book_id = %s
                    RETURNING book_id, title, author_name, publication_year, genre_id, copy_count
                """, (
                    title,
                    author_name,
                    publication_year,
                    genre_id,
                    copy_count,
                    book_id
                ))
                row = cursor.fetchone()
                return self._map_row(row) if row else None

    def delete(self, book_id: int) -> bool:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    DELETE FROM library.books
                    WHERE book_id = %s
                    RETURNING book_id
                """, (book_id,))
                return cursor.fetchone() is not None