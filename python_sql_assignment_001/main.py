import psycopg
from genre_dao import GenreDAO
from book_dao import BookDAO
from db_util import get_conn_string



#main
def main():
  with psycopg.connect(get_conn_string()) as conn:
    intialize_db(conn)
    genre_dao = GenreDAO(conn)
    book_dao = BookDAO(conn)



#helper function
def intialize_db(conn):
    """Initialize the database"""
    try:
        with conn.transaction():
            with open("ddl.sql","r") as file:
                sql = file.read
                with conn.cursor() as cur:
                    cur.execute(sql)
                    print("Setup successful")
                              
    except psycopg.Error as e:
        print(f"Database Setup Failed - Exception thrown: {e}")


#Insert at least two records into each table
#Demonstrate a read, update, and delete operation on at least one table


if __name__ == "__main__":
    main()

