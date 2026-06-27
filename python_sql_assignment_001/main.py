from psycopg.sql import SQL

from db import Database

if __name__ == "__main__":
    database: Database = Database()
    #create the tables
    with database.get_connection() as conn, open("create_tables.sql", "r") as ct:
        conn.execute(ct.read())



