# from datetime import date
from fastapi import FastAPI

from database import Database
from dao import GenreDAO, BookDAO, MemberDAO, LoanDAO
from crud import endpoints

app = FastAPI()

def initialize_db(db):
    with db.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Genre (
                genre_id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS Book (
                book_id SERIAL PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                author VARCHAR(100) NOT NULL,
                publication_year INTEGER NOT NULL,
                genre_id INTEGER NOT NULL REFERENCES Genre(genre_id),
                copy_count INTEGER NOT NULL CHECK (copy_count >= 0)
            );
            CREATE TABLE IF NOT EXISTS Member (
                member_id SERIAL PRIMARY KEY,
                full_name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                join_date DATE NOT NULL
            );
            CREATE TABLE IF NOT EXISTS Loan (
                loan_id SERIAL PRIMARY KEY,
                book_id INTEGER NOT NULL REFERENCES Book(book_id),
                member_id INTEGER NOT NULL REFERENCES Member(member_id),
                loan_date DATE NOT NULL,
                due_date DATE NOT NULL,
                return_date DATE
            );
            """
        )
    db.commit()
    
def trunc_DB(db):
    with db.cursor() as cur:
        cur.execute(
            """
            TRUNCATE TABLE Loan, Member, Book, Genre
            RESTART IDENTITY CASCADE;
            """
        )
    db.commit()
    
db = Database()
# trunc_DB(db)

initialize_db(db)

genre = GenreDAO(db)
book = BookDAO(db)
member = MemberDAO(db)
loan = LoanDAO(db)

endpoints(app, genre, book, member, loan)

    # genre_id = genre.create("Testing")
    # genre_id_other = genre.create("TEST")
    # print(genre.get_all())
    # genre.update(genre_id, "Science Fiction")
    # print(genre.get_by_id(genre_id))

    # book_id = book.create("Testing", "Veronica Roth", 2011, genre_id, 3)
    # book_id_other = book.create("TEST", "TEST", 1000, genre_id_other, 1)
    # print(book.get_all())
    # book.update(book_id, "Divergent", "Veronica Roth", 2011, genre_id, 3)
    # print(book.get_by_id(book_id))
    
    # member_id = member.create("Bob Ross", "example@gmail.com", date(2026, 6, 27))
    # member_id_other = member.create("TEST", "TEST", date(2000, 1, 1))
    # print(member.get_all())
    # member.update(member_id, "Bob Ross", "example@gmail.com", date(2026, 6, 27))
    # print(member.get_by_id(member_id))
    
    # loan_id = loan.create(book_id, member_id, date(2026, 6, 27), date(2026, 7, 8))
    # loan_id_other = loan.create(book_id_other, member_id_other, date(2000, 1, 1), date(2000, 1, 1))        
    # print(loan.get_all())
    # loan.update(loan_id, book_id, member_id, date(2026, 6, 27), date(2026, 7, 4), date(2026, 7, 1))
    # print(loan.get_by_id(loan_id))
    
    # loan.delete(loan_id)
    # loan.delete(loan_id_other)
    # member.delete(member_id)
    # member.delete(member_id_other)
    # book.delete(book_id)
    # book.delete(book_id_other)
    # genre.delete(genre_id)
    # genre.delete(genre_id_other)
    
    # print(loan.get_all())
    # print(member.get_all())
    # print(book.get_all())
    # print(genre.get_all())

    # db.close()
