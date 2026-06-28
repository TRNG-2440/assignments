import psycopg
from typing import LiteralString, cast
from db_util import get_conn_string

def initialize_db():
    with open("library.sql", "r") as f:
        ddl = f.read()
    with psycopg.connect(get_conn_string()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(cast(LiteralString, ddl))