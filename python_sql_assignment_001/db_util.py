import sqlite3
from contextlib import contextmanager

DB_NAME = "library.db"


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def initialize_db():
    with get_connection() as conn:
        conn.executescript("""
            DROP TABLE IF EXISTS Loan;
            DROP TABLE IF EXISTS Book;
            DROP TABLE IF EXISTS Member;
            DROP TABLE IF EXISTS Genre;

            CREATE TABLE Genre (
                genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );

            CREATE TABLE Book (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publication_year INTEGER NOT NULL,
                genre_id INTEGER NOT NULL,
                copy_count INTEGER NOT NULL,
                FOREIGN KEY (genre_id) REFERENCES Genre(genre_id)
            );

            CREATE TABLE Member (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                join_date TEXT NOT NULL
            );

            CREATE TABLE Loan (
                loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                loan_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                return_date TEXT,
                FOREIGN KEY (book_id) REFERENCES Book(book_id),
                FOREIGN KEY (member_id) REFERENCES Member(member_id)
            );
        """)