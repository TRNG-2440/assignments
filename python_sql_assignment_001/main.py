from psycopg.sql import SQL

from assignments.python_sql_assignment_001.librarydao import GenreDao
from assignments.python_sql_assignment_001.records import GenreRecord
from db import Database

if __name__ == "__main__":
    database: Database = Database()
    #create the tables
    with database.get_connection() as conn, open("create_tables.sql", "r") as ct:
        conn.execute(ct.read())
        #clear the tables (if they already existed)
        conn.execute("""
            TRUNCATE Genre CASCADE;
            TRUNCATE Book CASCADE;
            TRUNCATE Member CASCADE;
            TRUNCATE Loan CASCADE;
        """)

    genre_dao: GenreDao = GenreDao(database)

    fantasy_genre: GenreRecord = genre_dao.create(name="Fantasy")
    science_fiction_genre: GenreRecord = genre_dao.create(record=GenreRecord(genre_id=1, name="Science Fiction"))
    
    print("Create Fantasy -", fantasy_genre)
    print("Create Science Fiction -", science_fiction_genre)
    
    print("Get All -", genre_dao.get_all())
    print("Genre Fantasy -", genre_dao.get_by_id(fantasy_genre.genre_id))
    print("Delete Fantasy -", genre_dao.delete(fantasy_genre.genre_id))
    print("Genre Fantasy (will be None) -", genre_dao.get_by_id(fantasy_genre.genre_id))
    print("Get All -", genre_dao.get_all())

    print("Update Science Fiction to Sci-Fi -", genre_dao.update(genre_id=science_fiction_genre.genre_id, name="Sci-Fi"))
    print("Get Science Fiction -", genre_dao.get_by_id(science_fiction_genre.genre_id))

