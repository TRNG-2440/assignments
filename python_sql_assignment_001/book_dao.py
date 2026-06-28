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
# =============================================================================
class BookDAO:
    def __init__(self,conn):
        # Connection string is built once at instantiation from environment
        # variables loaded by db_util. All methods reuse this value.
        self.conn = conn


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
