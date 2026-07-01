import psycopg
from psycopg.rows import dict_row
from typing import Optional

from db_util import get_conn_string
from dao import GenreRecord


class GenreDAO:
    def __init__(self):
        self.conn_string = get_conn_string()

    def _map_row(self, row) -> GenreRecord:
        return GenreRecord(
            genre_id=row["genre_id"],
            genre_name=row["genre_name"]
        )

    def create(self, name: str) -> GenreRecord:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    INSERT INTO library.genres (genre_name)
                    VALUES (%s)
                    RETURNING genre_id, genre_name
                """, (name,))
                row = cursor.fetchone()
                return self._map_row(row)

    def get_by_id(self, genre_id: int) -> Optional[GenreRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    SELECT genre_id, genre_name
                    FROM library.genres
                    WHERE genre_id = %s
                """, (genre_id,))
                row = cursor.fetchone()
                return self._map_row(row) if row else None

    def get_all(self) -> list[GenreRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    SELECT genre_id, genre_name
                    FROM library.genres
                    ORDER BY genre_id
                """)
                rows = cursor.fetchall()
                return [self._map_row(row) for row in rows]

    def update(self, genre_id: int, name: str) -> Optional[GenreRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    UPDATE library.genres
                    SET genre_name = %s
                    WHERE genre_id = %s
                    RETURNING genre_id, genre_name
                """, (name, genre_id))
                row = cursor.fetchone()
                return self._map_row(row) if row else None

    def delete(self, genre_id: int) -> bool:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    DELETE FROM library.genres
                    WHERE genre_id = %s
                    RETURNING genre_id
                """, (genre_id,))
                return cursor.fetchone() is not None