from daos import *
import sqlite3

def main():
    conn = sqlite3.connect("python_sql_assignment_001/books.db")


    with open("python_sql_assignment_001/schema.sql") as f:
        conn.executescript(f.read())

    genre_dao = GenreDao(conn)
    book_dao = BookDAO(conn)
    member_dao = MemberDAO(conn)
    loan_dao = LoanDAO(conn)

    conn.close()


if __name__ == '__main__':
    main()