"""Database connection management and schema setup.

Connection settings are read from environment variables so the same code runs
against any PostgreSQL instance. Defaults match a local setup.
"""

import os

import psycopg2

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", "5432"),
    "dbname": os.environ.get("DB_NAME", "library"),
    "user": os.environ.get("DB_USER", "prachi"),
    "password": os.environ.get("DB_PASSWORD", "prachi"),
}

# Dropping first makes the demo repeatable. Remove the DROP block if running
# against a database that should persist.
SCHEMA_SQL = """
DROP TABLE IF EXISTS loan CASCADE;
DROP TABLE IF EXISTS book CASCADE;
DROP TABLE IF EXISTS member CASCADE;
DROP TABLE IF EXISTS genre CASCADE;

CREATE TABLE genre (
    genre_id SERIAL PRIMARY KEY,
    name     TEXT NOT NULL UNIQUE
);

CREATE TABLE book (
    book_id          SERIAL  PRIMARY KEY,
    title            TEXT    NOT NULL,
    author           TEXT    NOT NULL,
    publication_year INTEGER,
    genre_id         INTEGER REFERENCES genre (genre_id),
    copy_count       INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE member (
    member_id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    email     TEXT NOT NULL UNIQUE,
    join_date DATE NOT NULL
);

CREATE TABLE loan (
    loan_id     SERIAL  PRIMARY KEY,
    book_id     INTEGER NOT NULL REFERENCES book (book_id),
    member_id   INTEGER NOT NULL REFERENCES member (member_id),
    loan_date   DATE    NOT NULL,
    due_date    DATE    NOT NULL,
    return_date DATE
);
"""


def get_connection():
    """Open and return a new connection to the library database."""
    return psycopg2.connect(**DB_CONFIG)


def initialize_db(conn):
    """Create the four library tables."""
    with conn.cursor() as cur:
        cur.execute(SCHEMA_SQL)
    conn.commit()
