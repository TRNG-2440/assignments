from psycopg.rows import dict_row
from dataclasses import dataclass
from typing import Optional
from datetime import date

#dataclasses
@dataclass
class LoanRecord:
    loan_id: int
    book_id: int
    member_id: int
    loan_date: date
    due_date: date
    return_date: Optional[date]
   
## =============================================================================
# DAO CLASS
# =============================================================================
class LoanDAO:
    def __init__(self,conn):
        # Connection string is built once at instantiation from environment
        # variables loaded by db_util in main. All methods reuse this value.
        self._conn = conn


    def _map_row(self, row) -> LoanRecord:
            # Private helper that converts a psycopg Row (dict-style) into an
            # dataclass instance.

            return LoanRecord(
                loan_id=row["loan_id"],
                book_id=row["book_id"],
                member_id = row["member_id"],
                loan_date=row["loan_date"],
                due_date=row["due_date"],
                return_date = row["return_date"]
            )
    
    def get_all(self) -> list[LoanRecord]:
        # Retrieves every row from the Book table.
        # Returns an empty list if no records exist.
        with self._conn.transaction():
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "SELECT loan_id, book_id, member_id, loan_date, due_date, return_date FROM books.loan"
                )
                return [self._map_row(row) for row in cursor.fetchall()]
            
    def create(self, book_id:int, member_id:int, loan_date:date, due_date:date, return_date:Optional[date]=None) -> Optional[LoanRecord]:
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "INSERT INTO books.loan(book_id, member_id, loan_date, due_date,return_date) VALUES (%s,%s,%s,%s,%s) RETURNING *",
                    (book_id,member_id,loan_date,due_date,return_date)
                )
                row = cursor.fetchone()
                return self._map_row(row) if row else None
    
    def get_by_id(self, loan_id:int)-> Optional[LoanRecord]:  #return a single loan by its ID
        # Retrieves a single loan by primary key.
        # Returns None if no record with the given loan_id exists —
        with self._conn.transaction():
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "SELECT loan_id, book_id, member_id, loan_date, due_date, return_date FROM books.loan WHERE loan_id = %s",
                    (loan_id,)
                )
                row = cursor.fetchone()
                return self._map_row(row) if row else None
    
    def update(self, loan_id:int,book_id:int, member_id:int, loan_date:date, due_date:date, return_date:date) -> Optional[LoanRecord]:
        # Performs a full replacement of an existing laon record.
        # All fields are overwritten with the values provided in the record.
        # RETURNING retrieves the updated row directly — if nothing is returned,
        # no record with the given loan_id existed and None is returned to the caller.
        with self._conn.transaction():
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    UPDATE books.loan
                    SET book_id = %s, member_id = %s, loan_date = %s, due_date = %s, return_date = %s
                    WHERE loan_id = %s
                    RETURNING *
                    """,
                    (book_id, member_id, loan_date, due_date, return_date, loan_id)
                )
                row = cursor.fetchone()
                return self._map_row(row) if row else None
            
    def delete(self, loan_id: int) -> bool:
        # Deletes a loan record by primary key.
        # RETURNING loan_id is used to detect whether a row was actually deleted —
        # if fetchone() returns None, no record with the given loan_id existed.
        # Returns True if a record was deleted, False if no match was found.
        with self._conn.transaction():
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "DELETE FROM books.loan WHERE loan_id = %s RETURNING loan_id",
                    (loan_id,)
                )
                return cursor.fetchone() is not None
         



                
            
    
    
