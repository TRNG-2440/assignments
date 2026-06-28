import psycopg
from psycopg.rows import dict_row
from dataclasses import dataclass
from typing import Optional

#dataclasses
@dataclass
class GenreRecord:
    genre_id: int
    genre_name: str
   
## =============================================================================
# DAO CLASS
# =============================================================================
class GenreDAO:
    def __init__(self,conn):
        # Connection string is built once at instantiation from environment
        # variables loaded by db_util. All methods reuse this value.
        self.conn = conn


    def _map_row(self, row) -> GenreRecord:
            # Private helper that converts a psycopg Row (dict-style) into an
            # dataclass instance.

            return GenreRecord(
                genre_id=row["genre_id"],
                genre_name=row["genre_name"] 
            )
    
    def get_all(self) -> list[GenreRecord]:
        # Retrieves every row from the genre table.
        # Returns an empty list if no records exist.
        with self._conn.transaction():
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "SELECT genre_id, genre_name FROM books.genre"
                )
                return [self._map_row(row) for row in cursor.fetchall()]
            
    def create(self, genre_id:int, genre_name:str) -> Optional[GenreRecord]:
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "INSERT INTO books.genre(genre_id,genre_name) VALUES (%s,%s) RETURNING *",
                    (genre_id,genre_name)
                )
                row = cursor.fetchone()
                return self._map_row(row) if row else None
    
    def get_by_id(self, genre_id:int)-> Optional[GenreRecord]:  #return a single book by its ID
        # Retrieves a single employee by primary key.
        # Returns None if no record with the given emp_id exists —
        # the caller (endpoint handler) is responsible for raising a 404.
        with self._conn.transaction():
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "SELECT genre_id, genre_name FROM books.genre WHERE genre_id = %s",
                    (genre_id,)
                )
                row = cursor.fetchone()
                return self._map_row(row) if row else None
    
    def update(self, genre_id:int, genre_name:str) -> Optional[GenreRecord]:
        # Performs a full replacement of an existing genre record.
        # All fields are overwritten with the values provided in the record.
        # RETURNING retrieves the updated row directly — if nothing is returned,
        # no record with the given genre_id existed and None is returned to the caller.
        with self._conn.transaction():
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    UPDATE books.genre
                    SET genre_name = %s
                    WHERE genre_id = %s
                    RETURNING *
                    """,
                    (genre_name,genre_id,)
                )
                row = cursor.fetchone()
                return self._map_row(row) if row else None
            
    def delete(self, genre_id: int) -> bool:
        # Deletes a genre record by primary key.
        # RETURNING genre_id is used to detect whether a row was actually deleted —
        # if fetchone() returns None, no record with the given book_id existed.
        # Returns True if a record was deleted, False if no match was found.
        with self._conn.transaction():
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "DELETE FROM books.genre WHERE genre_id = %s RETURNING genre_id",
                    (genre_id,)
                )
                return cursor.fetchone() is not None
         



                
            
    
    
