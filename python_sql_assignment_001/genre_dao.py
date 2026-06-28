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
