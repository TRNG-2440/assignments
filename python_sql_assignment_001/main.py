from daos import *
import os
import sqlite3

def main():


    db = "python_sql_assignment_001/books.db"

    if os.path.exists(db):
        os.remove(db)

    conn = sqlite3.connect("db")


    with open("python_sql_assignment_001/schema.sql") as f:
        conn.executescript(f.read())

        genre_dao = GenreDao(conn)
        book_dao = BookDAO(conn)
        member_dao = MemberDAO(conn)
        loan_dao = LoanDAO(conn)

        genre_dao.create("Sci-Fi")
        genre_dao.create("Western")
        print(genre_dao.get_all())
        book_dao.create("Leviathan Wakes", "James S.A. Corey", 2011, 1, 3)
        book_dao.create("We Are Legion (We Are Bob)", "Dennis E. Taylor", 2016, 1, 4)
        book_dao.create("Steel Ball Run", "Hirohiki Araki", 2004, 2, 2)
        print(book_dao.get_all())
        member_dao.create("Vincent Wong", "wong@gmail.com", "2025-03-11")
        member_dao.create("Mark Doe", "doe@gmail.com", "2021-01-10")
        print(member_dao.get_all())

        loan_dao.create(1, 1, "2026-08-10", "2026-09-13")
        loan_dao.create(3, 2, "2011-04-17", "2011-06-06")
        print(loan_dao.get_active_loans())
        print(loan_dao.return_book(1, "2026-09-10"))
        print(loan_dao.get_active_loans())
        loan_dao.delete(1)
        print("After deletion:")
        print(loan_dao.get_active_loans())

    conn.close()


if __name__ == '__main__':
    main()