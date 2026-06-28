from psycopg.rows import dict_row
from dataclasses import dataclass
from typing import Optional

#dataclasses
@dataclass
class BookRecord:
    book_id: int
    title: str
    author: str
    pub_year: int
    genre_id: int
    copies: int
   
## =============================================================================
# DAO CLASS
# -`create(title, author, publication_year, genre_id, copy_count)` — insert a new book, return the created record
# -`get_by_id(book_id)` — return a single book by its ID
# -get_all()` — return all books
# -`update(book_id, title, author, publication_year, genre_id, copy_count)` — update all fields on a book, return the updated record
# -`delete(book_id)` — delete a book by its ID
# =============================================================================
class BookDAO:
    def __init__(self,conn):
        # Connection string is built once at instantiation from environment
        # variables loaded by db_util in main. All methods reuse this value.
        self._conn = conn


    def _map_row(self, row) -> BookRecord:
            # Private helper that converts a psycopg Row (dict-style) into an
            # dataclass instance.

            return BookRecord(
                book_id=row["book_id"],
                title=row["title"],
                author = row["author"],
                pub_year=row["pub_year"],
                genre_id=row["genre_id"],
                copies = row["copies"]
            )
    
    def get_all(self) -> list[BookRecord]:
        # Retrieves every row from the Book table.
        # Returns an empty list if no records exist.
        with self._conn.transaction():
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "SELECT book_id, title, author, pub_year,genre_id,copies FROM books.book"
                )
                return [self._map_row(row) for row in cursor.fetchall()]
            
    def create(self, title:str, author:str, pub_year:int, genre_id:int, copies:int) -> Optional[BookRecord]:
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "INSERT INTO books.book(title, author, pub_year,genre_id,copies) VALUES (%s,%s,%s,%s,%s) RETURNING *",
                    (title,author,pub_year,genre_id,copies)
                )
                row = cursor.fetchone()
                return self._map_row(row) if row else None
    
    def get_by_id(self, book_id:int)-> Optional[BookRecord]:  #return a single book by its ID
        # Retrieves a single employee by primary key.
        # Returns None if no record with the given emp_id exists —
        # the caller (endpoint handler) is responsible for raising a 404.
        with self._conn.transaction():
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "SELECT book_id, title, author, pub_year,genre_id,copies FROM books.book WHERE book_id = %s",
                    (book_id,)
                )
                row = cursor.fetchone()
                return self._map_row(row) if row else None
    
    def update(self, book_id:int,title:str, author:str, pub_year:int, genre_id:int, copies:int) -> Optional[BookRecord]:
        # Performs a full replacement of an existing Book record.
        # All fields are overwritten with the values provided in the record.
        # RETURNING retrieves the updated row directly — if nothing is returned,
        # no record with the given book_id existed and None is returned to the caller.
        with self._conn.transaction():
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    UPDATE books.book
                    SET title = %s, author = %s, pub_year = %s, genre_id =%s,copies = %s
                    WHERE book_id = %s
                    RETURNING *
                    """,
                    (title, author, pub_year, genre_id,copies,book_id)
                )
                row = cursor.fetchone()
                return self._map_row(row) if row else None
            
    def delete(self, book_id: int) -> bool:
        # Deletes a book record by primary key.
        # RETURNING book_id is used to detect whether a row was actually deleted —
        # if fetchone() returns None, no record with the given book_id existed.
        # Returns True if a record was deleted, False if no match was found.
        # The caller (endpoint handler) uses this to decide whether to raise a 404.
        with self._conn.transaction():
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "DELETE FROM books.book WHERE book_id = %s RETURNING book_id",
                    (book_id,)
                )
                return cursor.fetchone() is not None
         



                
            
    
    
