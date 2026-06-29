import sqlite3

DB_NAME = "data.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def initialize_db():
    schema = """
    CREATE TABLE  Genre (
        genre_id INTEGER PRIMARY KEY,
        name VARCHAR UNIQUE
    );

    CREATE TABLE Book (
        book_id INTEGER PRIMARY KEY,
        title VARCHAR(100),
        author VARCHAR(100),
        publication_year INTEGER,
        genre_id INTEGER,
        copy_count INTEGER,
        FOREIGN KEY (genre_id) REFERENCES Genre(genre_id)
    );

    CREATE TABLE Member (
        member_id INTEGER PRIMARY KEY,
        full_name VARCHAR(100),
        email VARCHAR,
        join_date DATE
    );

    CREATE TABLE Loan (
        loan_id INTEGER PRIMARY KEY,
        book_id INTEGER,
        member_id INTEGER,
        loan_date DATE,
        due_date DATE,
        return_date DATE,
        FOREIGN KEY (book_id) REFERENCES Book(book_id),
        FOREIGN KEY (member_id) REFERENCES Member(member_id)
    );
    """
    with get_connection() as conn:
        conn.executescript(schema)