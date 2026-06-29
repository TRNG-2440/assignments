import psycopg
from psycopg.rows import dict_row
from connection import conn_string
from datetime import date
from dao import GenreDAO, BookDAO, MemberDOA, LoanDOA

def initialize_db():
    with psycopg.connect(conn_string()) as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("CREATE SCHEMA IF NOT EXISTS library")
            cursor.execute("""CREATE TABLE IF NOT EXISTS library.genre (
                           genre_id SERIAL PRIMARY KEY,
                           genre_name VARCHAR NOT NULL
                           );""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS library.book (
                           book_id SERIAL PRIMARY KEY,
                           title VARCHAR NOT NULL,
                           author_name VARCHAR NOT NULL,
                           publication_year VARCHAR NOT NULL,
                           genre_id INT REFERENCES library.genre(genre_id),
                           total_copies INT NOT NULL
                           );""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS library.member (
                           member_id SERIAL PRIMARY KEY,
                           member_name VARCHAR NOT NULL,
                           email VARCHAR NOT NULL,
                           join_date DATE NOT NULL
                           );""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS library.loan (
                           loan_id SERIAL PRIMARY KEY,
                           book_id INT REFERENCES library.book(book_id),
                           member_id INT REFERENCES library.member(member_id),
                           loan_date DATE NOT NULL,
                           due_date DATE NOT NULL,
                           return_date DATE
                           );""")
            

initialize_db()


genre = GenreDAO()
book = BookDAO()
member = MemberDOA()
loan = LoanDOA()

# inserting rows into tables
print(f"Genre created: \n{genre.create("Sci-Fi")}")
print(f"Genre created: \n{genre.create("Fantasy")}\n")

print(f"Book Created: \n{book.create("Empire of Silence", "Christopher Rucchio", "2018", 1, 10)}")
print(f"Book Created: \n{book.create("The Hobbit", "J.R.R. Tolkien", "1937", 2, 5)}\n")

print(f"Member Created: \n{member.create("Alex D.", "alex@gmail.com", date(2025, 12, 15))}")
print(f"Member Created: \n{member.create("Nate M.", "nate@gmail.com", date(2023, 5, 20))}\n")

print(f"Loan Created: \n{loan.create(2, 1, date(2026, 6, 25), date(2026, 7, 11))}")
print(f"Loan Created: \n{loan.create(1, 2, date(2026, 6, 20), date(2026, 7, 3))}\n")

# read, update, delete operations
print("All Loans: ")
print(loan.get_all())
print("****"*5)
print("2nd Loan: ")
print(loan.get_by_id(2))
print("****"*5)
print("Return 2nd Loan on Today's Date")
print(loan.return_book(2, date.today()))
print("****"*5)
print("Active Loans: ")
print(loan.get_active_loans())
print("****"*5)
print("Delete 1st loan: ")
loan.delete(1)
print("Show all loans: ")
print(loan.get_all())