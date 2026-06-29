import psycopg
from genre_dao import GenreDAO
from book_dao import BookDAO
from loan_dao import LoanDAO
from member_dao import MemberDAO
from db_util import get_conn_string
from datetime import datetime
import os



#main
def main():
  with psycopg.connect(get_conn_string()) as conn:
    intialize_db(conn)

    book_dao = BookDAO(conn)
    genre_dao = GenreDAO(conn)
    loan_dao = LoanDAO(conn)
    member_dao = MemberDAO(conn)

    #add at least two records into each table
    rom_genre = genre_dao.create("Romance")
    fan_genre = genre_dao.create("Fantasy")

    book_1 = book_dao.create("Jane Eyre","Charlotte Bronte",1847,rom_genre.genre_id,1)
    book_2 = book_dao.create("The Hobbit","J.R.R. Tolkien",1847,fan_genre.genre_id,2)
    book_3 = book_dao.create("Twilight","Stephenie Meyer",2005,rom_genre.genre_id,5)

    date_joined_1 = datetime.strptime("2026-01-28", "%Y-%m-%d").date()  
    date_joined_2 = datetime.strptime("2024-08-01", "%Y-%m-%d").date()  
    loan_date_1 = datetime.strptime("2026-03-03", "%Y-%m-%d").date() 
    loan_date_2 = datetime.strptime("2025-01-05", "%Y-%m-%d").date() 
    due_date_1 = datetime.strptime("2026-05-28", "%Y-%m-%d").date() 
    due_date_2 = datetime.strptime("2025-03-15", "%Y-%m-%d").date() 
    return_date_1 = datetime.strptime("2025-04-15", "%Y-%m-%d").date() 
    #no return date 2 to check null is allowed

    member_1 = member_dao.create("Suelem Audelo", "my_email@gmail.com", date_joined_1)
    member_2 = member_dao.create("Karen Reyes", "karen_email@gmail.com", date_joined_2)

    loan_dao.create(book_1.book_id,member_1.member_id,loan_date_1,due_date_1,return_date_1)
    loan_dao.create(book_2.book_id,member_2.member_id,loan_date_2,due_date_2)

    
    #Demonstrate a read, update, and delete operation on at least one table
    book_read = book_dao.get_by_id(book_1.book_id)

    print(book_read)

    book_updated = book_dao.update(book_1.book_id,"The Chronicles of Narnia","C.S. Lewis",1956,fan_genre.genre_id,3)

    print(book_updated)

    deleted = book_3.book_id
    book_deleted = book_dao.delete(deleted) #deleted extra book

    if book_deleted:
        print(f"Book id {deleted} has been deleted.")
    


#helper function
def intialize_db(conn):
    """Initialize the database"""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ddl_path = os.path.join(script_dir, "ddl.sql")
    try:
        with conn.transaction():
            with open(ddl_path,"r") as file:
                sql = file.read()
                with conn.cursor() as cur:
                    cur.execute(sql)
                    print("Setup successful")
                              
    except psycopg.Error as e:
        print(f"Database Setup Failed - Exception thrown: {e}")



#Demonstrate a read, update, and delete operation on at least one table


if __name__ == "__main__":
    main()

