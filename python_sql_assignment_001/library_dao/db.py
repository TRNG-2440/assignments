import psycopg
from psycopg.rows import dict_row


DB_CONFIG = {
    "db_name": "library_db",
    "user": "postgres",
    "password": "your_password",
    "host": "localhost",
    "port": 5432,

}

def get_connection():
    return psycopg.connect(**DB_CONFIG, row_factory= dict_row)


def initialize_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """"
                CREATE TABLE genre(
                    genre_id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL UNIQUE
                );

                CREATE TABLE book(
                    book_id SERIAL PRIMARY KEY,
                    title VARCHAR(255),
                    author VARCHAR(255),
                    genre_id INT REFERENCES genre(genre_id),
                    copy_count INT

                );

                CREATE TABLE member(
                    member_id SERIAL PRIMARY KEY,
                    full_name VARCHAR(255),
                    email VARCHAR(255),
                    join_date DATE,

                );

                CREATE TABLE loan(
                    loan_id SERIAL PRIMARY KEY,
                    book_id INT REFERENCES book(book_id),
                    member_id INT REFERENCES member(member_id),
                    loan_date DATE,
                    due_date DATE,
                    return_date DATE
                )

                """


            )