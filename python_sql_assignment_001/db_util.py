import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

def connection_details() -> str:
    """
    returns string with db connection info
        DB_HOST
        DB_NAME
        DB_USER
        DB_PASSWORD
        DB_PORT
    """
    return (
        f"host={os.environ.get('DB_HOST')} "
        f"dbname={os.environ.get('DB_NAME')} "
        f"user={os.environ.get('DB_USER')} "
        f"password={os.environ.get('DB_PASSWORD')} "
        f"port={os.environ.get('DB_PORT')}"
    )

def del_schema():
    with psycopg.connect(connection_details()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DROP SCHEMA IF EXISTS lfields001 CASCADE;
                """
            )


def init_db():
    with psycopg.connect(connection_details()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE SCHEMA IF NOT EXISTS lfields001;

                CREATE TABLE IF NOT EXISTS lfields001.Genre (
                    genre_id SERIAL PRIMARY KEY,
                    genre_name VARCHAR(32)
                );

                CREATE TABLE IF NOT EXISTS lfields001.Book (
                    book_id SERIAL PRIMARY KEY,
                    genre_id INT NOT NULL,
                    title VARCHAR(64),
                    author VARCHAR(64),
                    publication_year SMALLINT,
                    inventory SMALLINT,
                    CONSTRAINT genre_id_fk FOREIGN KEY (genre_id) REFERENCES lfields001.Genre(genre_id)
                    ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS lfields001.Member (
                    member_id SERIAL PRIMARY KEY,
                    member_name VARCHAR(64),
                    email VARCHAR(64),
                    date_joined DATE
                );

                CREATE TABLE IF NOT EXISTS lfields001.Loan (
                    loan_id SERIAL PRIMARY KEY,
                    book_id INT NOT NULL,
                    member_id INT NOT NULL,
                    date_loaned DATE,
                    date_due DATE NOT NULL,
                    date_returned DATE DEFAULT NULL,
                    CONSTRAINT book_id_fk FOREIGN KEY (book_id) REFERENCES lfields001.Book(book_id),
                    CONSTRAINT member_id_fk FOREIGN KEY (member_id) REFERENCES lfields001.Member(member_id)
                    ON DELETE CASCADE
                );
                """
            )