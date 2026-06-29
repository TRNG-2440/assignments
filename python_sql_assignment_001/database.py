import sqlite3

def get_connection():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def initialize_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Genre (
            genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS Book (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publication_year INTEGER NOT NULL,
            genre_id INTEGER NOT NULL,
            copy_count INTEGER NOT NULL,
            FOREIGN KEY (genre_id) REFERENCES Genre(genre_id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS Member (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            join_date TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS Loan (
            loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            loan_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            FOREIGN KEY (book_id) REFERENCES Book(book_id),
            FOREIGN KEY (member_id) REFERENCES Member(member_id)
        )
    """)

    conn.commit()