from psycopg.rows import dict_row
from dataclasses import dataclass
from typing import Optional
from datetime import date
#dataclasses
@dataclass
class MemberRecord:
    member_id: int
    full_name: str
    email: str
    date_joined: date
    
   
## =============================================================================
# DAO CLASS
# =============================================================================
class MemberDAO:
    def __init__(self,conn):
        # Connection string is built once at instantiation from environment
        # variables loaded by db_util in main. All methods reuse this value.
        self._conn = conn


    def _map_row(self, row) -> MemberRecord:
            # Private helper that converts a psycopg Row (dict-style) into an
            # dataclass instance.

            return MemberRecord(
                member_id=row["member_id"],
                full_name=row["full_name"],
                email = row["email"],
                date_joined=row["date_joined"]
            )
    
    def get_all(self) -> list[MemberRecord]:
        # Retrieves every row from the Member table.
        # Returns an empty list if no records exist.
        with self._conn.transaction():
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "SELECT member_id, full_name, email, date_joined FROM books.member"
                )
                return [self._map_row(row) for row in cursor.fetchall()]
            
    def create(self, full_name:str, email:str,date_joined:date) -> Optional[MemberRecord]:
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "INSERT INTO books.member(full_name,email,date_joined) VALUES (%s,%s,%s) RETURNING *",
                    (full_name,email,date_joined)
                )
                row = cursor.fetchone()
                return self._map_row(row) if row else None
    
    def get_by_id(self, member_id:int)-> Optional[MemberRecord]:  #return a single member by its ID
        # Retrieves a single member by primary key.
        # Returns None if no record with the given member_id exists —
        # the caller (endpoint handler) is responsible for raising a 404.
        with self._conn.transaction():
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "SELECT member_id, full_name, email, date_joined FROM books.member WHERE member_id = %s",
                    (member_id,)
                )
                row = cursor.fetchone()
                return self._map_row(row) if row else None
    
    def update(self, member_id:int,full_name:str, email:str, date_joined) -> Optional[MemberRecord]:
        # Performs a full replacement of an existing member record.
        # All fields are overwritten with the values provided in the record.
        # RETURNING retrieves the updated row directly — if nothing is returned,
        # no record with the given member_id existed and None is returned to the caller.
        with self._conn.transaction():
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    UPDATE books.member
                    SET full_name = %s, email = %s, date_joined = %s
                    WHERE member_id = %s
                    RETURNING *
                    """,
                    (full_name, email, date_joined,member_id)
                )
                row = cursor.fetchone()
                return self._map_row(row) if row else None
            
    def delete(self, member_id: int) -> bool:
        # Deletes a member record by primary key.
        # RETURNING member_id is used to detect whether a row was actually deleted —
        # if fetchone() returns None, no record with the given book_id existed.
        # Returns True if a record was deleted, False if no match was found.
        with self._conn.transaction():
            with self._conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "DELETE FROM books.member WHERE member_id = %s RETURNING member_id",
                    (member_id,)
                )
                return cursor.fetchone() is not None
         



                
            
    
    
