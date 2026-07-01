import psycopg
from db_util import get_conn_string


def initialize_db():
    with psycopg.connect(get_conn_string()) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS library;
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS library.genres (
                    genre_id SERIAL PRIMARY KEY,
                    genre_name VARCHAR(100) NOT NULL,
                    CONSTRAINT uq_genres_genre_name UNIQUE (genre_name)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS library.members (
                    member_id SERIAL PRIMARY KEY,
                    full_name VARCHAR(150) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    join_date DATE NOT NULL,
                    CONSTRAINT uq_members_email UNIQUE (email)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS library.books (
                    book_id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    author_name VARCHAR(255) NOT NULL,
                    publication_year INT NOT NULL,
                    genre_id INT NOT NULL,
                    copy_count INT NOT NULL,
                    CONSTRAINT chk_books_publication_year
                        CHECK (publication_year > 0),
                    CONSTRAINT chk_books_copy_count
                        CHECK (copy_count >= 0),
                    CONSTRAINT fk_books_genre
                        FOREIGN KEY (genre_id)
                        REFERENCES library.genres (genre_id)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS library.loans (
                    loan_id SERIAL PRIMARY KEY,
                    book_id INT NOT NULL,
                    member_id INT NOT NULL,
                    loan_date DATE NOT NULL,
                    due_date DATE NOT NULL,
                    return_date DATE,
                    CONSTRAINT chk_loans_due_date
                        CHECK (due_date >= loan_date),
                    CONSTRAINT chk_loans_return_date
                        CHECK (return_date IS NULL OR return_date >= loan_date),
                    CONSTRAINT fk_loans_book
                        FOREIGN KEY (book_id)
                        REFERENCES library.books (book_id),
                    CONSTRAINT fk_loans_member
                        FOREIGN KEY (member_id)
                        REFERENCES library.members (member_id)
                );
            """)

    print("Database schema and tables created successfully.")


if __name__ == "__main__":
    initialize_db()