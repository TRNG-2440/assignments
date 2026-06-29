import psycopg
from psycopg.rows import dict_row
from dataclasses import dataclass
from typing import Optional
from connection import conn_string
from datetime import date

@dataclass
class Genre:
    genre_id: int
    genre_name: str

@dataclass
class Book:
    book_id: int
    title: str
    author_name: str
    publication_year: str
    genre_id: int
    total_copies: int

@dataclass
class Member:
    member_id: int
    member_name: str
    email: str
    join_date: date

@dataclass
class Loan:
    loan_id: int
    book_id: int
    member_id: int
    loan_date: date
    due_date: date
    return_date: date

class GenreDAO:
    def create(self, name: str):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    INSERT INTO library.genre (genre_name) VALUES (%s)
                    RETURNING genre_id;
                    """, (name,)
                )
                new_id = cursor.fetchone()["genre_id"]
                return Genre(
                    genre_id=new_id,
                    genre_name=name
                )
            
    def get_by_id(self, genre_id: int):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT * FROM library.genre
                    WHERE genre_id = %s
                    """, (genre_id, )
                )
                row = cursor.fetchone()
                return Genre(
                    genre_id=row["genre_id"],
                    genre_name=row["genre_name"]
                )
            
    def get_all(self):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT * FROM library.genre
                    """
                )
                all_rows = cursor.fetchall()
                all_genres = []
                for row in all_rows:
                    all_genres.append(Genre (
                        genre_id=row["genre_id"],
                        genre_name=row["genre_name"]
                    ))

                return all_genres
            
    def update(self, genre_id: int, name: str):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    UPDATE library.genre
                    SET genre_name = %s
                    WHERE genre_id = %s
                    RETURNING *
                    """, (name, genre_id)
                )
                row = cursor.fetchone()
                return Genre(
                    genre_id=row["genre_id"],
                    genre_name=row["genre_name"]
                )
            
    def delete(self, genre_id: int):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    DELETE FROM library.genre
                    WHERE genre_id = %s
                    """, (genre_id, )
                )

class BookDAO:
    def create(self, title: str, author: str, publication_year: str, genre_id: int, copy_count: int):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    INSERT INTO library.book (title, author_name, publication_year, genre_id, total_copies) 
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING book_id;
                    """, (title, author, publication_year, genre_id, copy_count)
                )
                new_id = cursor.fetchone()["book_id"]
                return Book(
                    book_id=new_id,
                    title=title,
                    author_name=author,
                    publication_year=publication_year,
                    genre_id=genre_id,
                    total_copies=copy_count
                )
            
    def get_by_id(self, book_id: int):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT * FROM library.book
                    WHERE book_id = %s
                    """, (book_id, )
                )
                row = cursor.fetchone()
                return Book(
                    book_id=row["book_id"],
                    title=row["title"],
                    author_name=row["author_name"],
                    publication_year=row["publication_year"],
                    genre_id=row["genre_id"],
                    total_copies=row["total_copies"]
                )
            
    def get_all(self):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT * FROM library.book
                    """
                )
                all_rows = cursor.fetchall()
                all_books = []
                for row in all_rows:
                    all_books.append( Book(
                        book_id=row["book_id"],
                        title=row["title"],
                        author_name=row["author_name"],
                        publication_year=row["publication_year"],
                        genre_id=row["genre_id"],
                        total_copies=row["total_copies"]
                    ))

                return all_books
    
    def update(self, book_id: int, title: str, author: str, publication_year: str, genre_id: int, copy_count: int):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    UPDATE library.book
                    SET title = %s, author_name = %s, publication_year = %s, genre_id = %s, total_copies = %s
                    WHERE book_id = %s
                    RETURNING *
                    """, (title, author, publication_year, genre_id, copy_count, book_id)
                )
                row = cursor.fetchone()
                return Book(
                    book_id=row["book_id"],
                    title=row["title"],
                    author_name=row["author_name"],
                    publication_year=row["publication_year"],
                    genre_id=row["genre_id"],
                    total_copies=row["total_copies"]
                )
            
    def delete(self, book_id: int):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    DELETE FROM library.book
                    WHERE book_id = %s
                    """, (book_id, )
                )


class MemberDOA:
    def create(self, member_name: str, email: str, join_date: date):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    INSERT INTO library.member (member_name, email, join_date) 
                    VALUES (%s, %s, %s)
                    RETURNING member_id;
                    """, (member_name, email, join_date)
                )
                new_id = cursor.fetchone()["member_id"]
                return Member(
                    member_id=new_id,
                    member_name=member_name,
                    email=email,
                    join_date=join_date
                )
            
    def get_by_id(self, member_id: int):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT * FROM library.member
                    WHERE member_id = %s
                    """, (member_id, )
                )
                row = cursor.fetchone()
                return Member(
                    member_id=row["member_id"],
                    member_name=row["member_name"],
                    email=row["email"],
                    join_date=row["join_date"]
                )
            
    def get_all(self):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT * FROM library.member
                    """
                )
                all_rows = cursor.fetchall()
                all_members = []
                for row in all_rows:
                    all_members.append( Member(
                        member_id=row["member_id"],
                        member_name=row["member_name"],
                        email=row["email"],
                        join_date=row["join_date"]
                    ))

                return all_members
            
    def update(self, member_id: int, member_name: str, email: str, join_date: date):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    UPDATE library.member
                    SET member_name = %s, email = %s, join_date = %s
                    WHERE member_id = %s
                    RETURNING *
                    """, (member_name, email, join_date, member_id)
                )
                row = cursor.fetchone()
                return Member(
                    member_id=row["member_id"],
                    member_name=row["member_name"],
                    email=row["email"],
                    join_date=row["join_date"]
                )
            
    def delete(self, member_id: int):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    DELETE FROM library.member
                    WHERE member_id = %s
                    """, (member_id, )
                )


class LoanDOA:
    def create(self, book_id: int, member_id: int, loan_date: date, due_date: date):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    INSERT INTO library.loan (book_id, member_id, loan_date, due_date) 
                    VALUES (%s, %s, %s, %s)
                    RETURNING loan_id;
                    """, (book_id, member_id, loan_date, due_date)
                )
                new_id = cursor.fetchone()["loan_id"]
                return Loan(
                    loan_id=new_id,
                    book_id=book_id,
                    member_id=member_id,
                    loan_date=loan_date,
                    due_date=due_date,
                    return_date=None
                )
            
    def get_by_id(self, loan_id: int):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT * FROM library.loan
                    WHERE loan_id = %s
                    """, (loan_id, )
                )
                row = cursor.fetchone()
                return Loan(
                    loan_id=row["loan_id"],
                    book_id=row["book_id"],
                    member_id=row["member_id"],
                    loan_date=row["loan_date"],
                    due_date=row["due_date"],
                    return_date=row["return_date"]
                )
            
    def get_all(self):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT * FROM library.loan
                    """
                )
                all_rows = cursor.fetchall()
                all_loans = []
                for row in all_rows:
                    all_loans.append( Loan(
                        loan_id=row["loan_id"],
                        book_id=row["book_id"],
                        member_id=row["member_id"],
                        loan_date=row["loan_date"],
                        due_date=row["due_date"],
                        return_date=row["return_date"]
                    ))

                return all_loans
            
    def get_active_loans(self):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT * FROM library.loan
                    WHERE return_date IS NULL
                    """
                )
                all_rows = cursor.fetchall()
                active_loans = []
                for row in all_rows:
                    active_loans.append( Loan(
                        loan_id=row["loan_id"],
                        book_id=row["book_id"],
                        member_id=row["member_id"],
                        loan_date=row["loan_date"],
                        due_date=row["due_date"],
                        return_date=row["return_date"]
                    ))

                return active_loans
            
    def return_book(self, loan_id: int, return_date: date):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    UPDATE library.loan
                    SET return_date = %s
                    WHERE loan_id = %s
                    RETURNING *
                    """, (return_date, loan_id)
                )
                row = cursor.fetchone()
                return Loan(
                    loan_id=row["loan_id"],
                    book_id=row["book_id"],
                    member_id=row["member_id"],
                    loan_date=row["loan_date"],
                    due_date=row["due_date"],
                    return_date=row["return_date"]
                )
            
    def delete(self, loan_id: int):
        with psycopg.connect(conn_string()) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    DELETE FROM library.loan
                    WHERE loan_id = %s
                    """, (loan_id, )
                )