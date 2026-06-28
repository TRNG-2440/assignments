from datetime import date
import psycopg
from psycopg.rows import dict_row
from dataclasses import dataclass
from typing import Optional
from db_util import get_conn_string

# ============================================================
# DAO Classes for Genre, Book, Member, and Loan
# ============================================================

# ============================================================
# Database Model for Genre
# ============================================================
@dataclass
class GenreRecord:
    genre_id: int
    genre_name: str

# ============================================================
# Genre DAO Class
# ============================================================
class GenreDAO:
    def __init__(self):
        self.conn_string = get_conn_string()

    def map_row(self, row) -> GenreRecord:
        # convert Row object into GenreRecord dataclass instance
        return GenreRecord(
            genre_id=row["genre_id"],
            genre_name=row["genre_name"]
        )

    def create(self, genre_name: str) -> GenreRecord:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    INSERT INTO library.genre (genre_name)
                    VALUES (%s)
                    RETURNING genre_id
                    """,
                    (genre_name, )
                )
                return self.map_row(cursor.fetchone())
    
    def get_all(self) -> list[GenreRecord]:
        # retrieve every row from genre table
        # returns empty list if there are no records
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT genre_id, genre_name FROM library.genre")
                return [self.map_row(row) for row in cursor.fetchall()]

    def get_by_id(self, genre_id: int) -> Optional[GenreRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "SELECT genre_id, genre_name FROM library.genre WHERE genre_id = %s",
                    (genre_id, )
                )
                row = cursor.fetchone()
                return self.map_row(row) if row else None
    
    def update(self, genre_id: int, name: str) -> Optional[GenreRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    UPDATE library.genre
                    SET genre_name = %s
                    WHERE genre_id = %s
                    RETURNING genre_id, genre_name
                    """,
                    (name, genre_id)
                )
                row = cursor.fetchone()
                return self.map_row(row) if row else None

    def delete(self, genre_id: int) -> bool:
        try:
            with psycopg.connect(self.conn_string) as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    cursor.execute(
                        "DELETE FROM library.genre WHERE genre_id = %s RETURNING genre_id",
                        (genre_id, )
                    )
                    return cursor.fetchone() is not None
        except psycopg.errors.ForeignKeyViolation as e:
            raise ValueError(f"cannot remove genre_id {genre_id} as it appears in library.book") from e

# ============================================================
# Database Model for Book
# ============================================================
@dataclass
class BookRecord:
    book_id: int
    title: str
    author: str
    publication_year: int
    genre_id: int
    copy_count: int

# ============================================================
# Book DAO Class
# ============================================================
class BookDAO:
    def __init__(self):
        self.conn_string = get_conn_string()

    def map_row(self, row) -> BookRecord:
        return BookRecord(
            book_id = row["book_id"],
            title = row["title"],
            author = row["author"],
            publication_year = row["publication_year"],
            genre_id = row["genre_id"],
            copy_count = row["copy_count"]
        )
    
    def create(self, title: str, author: str,
            publication_year: int, genre_id: int, copy_count: int) -> BookRecord:
        try:
            with psycopg.connect(self.conn_string) as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    cursor.execute(
                        """
                        INSERT INTO library.book (title, author, publication_year, genre_id, copy_count)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING book_id, title, author, publication_year, genre_id, copy_count
                        """,
                        (title, author, publication_year, genre_id, copy_count)
                    )
                    return self.map_row(cursor.fetchone())
        except psycopg.errors.ForeignKeyViolation as e:
            raise ValueError(f"genre_id {genre_id} does not exist in library.genre") from e
        except psycopg.errors.CheckViolation as e:
            raise ValueError(f"copy_count {copy_count} is invalid, please select a non-negative integer") from e

    def get_by_id(self, book_id: int) -> Optional[BookRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT * FROM library.book WHERE book_id = %s", (book_id,))
                row = cursor.fetchone()
                return self.map_row(row) if row else None

    def get_all(self) -> list[BookRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT * FROM library.book")
                return [self.map_row(row) for row in cursor.fetchall()]  

    def update(self, book_id: int, title: str, author: str, publication_year: int,
                genre_id: int, copy_count: int) -> Optional[BookRecord]:
        try:
            with psycopg.connect(self.conn_string) as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    cursor.execute(
                        """
                        UPDATE library.book
                        SET title = %s, author = %s, publication_year = %s, genre_id = %s, copy_count = %s
                        WHERE book_id = %s
                        RETURNING book_id, title, author, publication_year, genre_id, copy_count
                        """,
                        (title, author, publication_year, genre_id, copy_count, book_id)
                    )
                    row = cursor.fetchone()
                    return self.map_row(row) if row else None
        except psycopg.errors.ForeignKeyViolation as e:
            raise ValueError(f"genre_id {genre_id} does not exist in library.genre") from e
        except psycopg.errors.CheckViolation as e:
            raise ValueError(f"copy_count {copy_count} is invalid, please select a non-negative integer") from e
    
    def delete(self, book_id: int) -> bool:
        try:
            with psycopg.connect(self.conn_string) as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    cursor.execute("DELETE FROM library.book WHERE book_id = %s RETURNING book_id", (book_id, ))
                    return cursor.fetchone() is not None
        except psycopg.errors.ForeignKeyViolation as e:
            raise ValueError(f"cannot remove book_id {book_id} as it appears in library.loan") from e

# ============================================================
# Database Model for Member
# ============================================================
@dataclass
class MemberRecord:
    member_id: int
    member_name: str
    email: str
    join_date: date

# ============================================================
# Member DAO Class
# ============================================================
class MemberDAO:
    def __init__(self):
        self.conn_string = get_conn_string()

    def map_row(self, row) -> MemberRecord:
        return MemberRecord(
            member_id = row["member_id"],
            member_name = row["member_name"],
            email = row["email"],
            join_date = row["join_date"]
        )

    def create(self, full_name: str, email: str, join_date: date) -> MemberRecord:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    INSERT INTO library.member (member_name, email, join_date)
                    VALUES (%s, %s, %s)
                    RETURNING member_id, member_name, email, join_date
                    """,
                    (full_name, email, join_date)
                )
                return self.map_row(cursor.fetchone())
    
    def get_by_id(self, member_id: int) -> Optional[MemberRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT * FROM library.member WHERE member_id = %s", (member_id,))
                row = cursor.fetchone()
                return self.map_row(row) if row else None
    
    def get_all(self) -> list[MemberRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT * FROM library.member")
                return [self.map_row(row) for row in cursor.fetchall()]

    def update(self, member_id: int, full_name: str, email: str, join_date: date) -> Optional[MemberRecord]:
        try:
            with psycopg.connect(self.conn_string) as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    cursor.execute(
                        """
                        UPDATE library.member
                        SET member_name = %s, email = %s, join_date = %s
                        WHERE member_id = %s
                        RETURNING member_id, member_name, email, join_date
                        """,
                        (full_name, email, join_date, member_id)
                    )
                    row = cursor.fetchone()
                    return self.map_row(row) if row else None
        except psycopg.errors.ForeignKeyViolation as e:
            raise ValueError(f"member_id {member_id} is not in library.member") from e
    
    def delete(self, member_id: int) -> bool:
        try:
            with psycopg.connect(self.conn_string) as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    cursor.execute("DELETE FROM library.member WHERE member_id = %s RETURNING member_id", (member_id,))
                    return cursor.fetchone() is not None
        except psycopg.errors.ForeignKeyViolation as e:
            raise ValueError(f"cannot remove member_id {member_id} as it appears in library.loan") from e

# ============================================================
# Database Model for Loan
# ============================================================
@dataclass
class LoanRecord:
    loan_id: int
    book_id: int
    member_id: int
    loan_date: date
    due_date: date
    return_date: date | None

# ============================================================
# Loan DAO Class
# ============================================================
class LoanDAO:
    def __init__(self):
        self.conn_string = get_conn_string()

    def map_row(self, row) -> LoanRecord:
        return LoanRecord(
            loan_id = row["loan_id"],
            book_id = row["book_id"],
            member_id = row["member_id"],
            loan_date = row["loan_date"],
            due_date = row["due_date"],
            return_date = row["return_date"]
        )
    
    def get_by_id(self, loan_id: int) -> Optional[LoanRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT * FROM library.loan WHERE loan_id = %s", (loan_id,))
                row = cursor.fetchone()
                return self.map_row(row) if row else None
    
    def get_all(self) -> list[LoanRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT * FROM library.loan")
                return [self.map_row(row) for row in cursor.fetchall()]
    
    def get_active_loans(self) -> list[LoanRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT * FROM library.loan WHERE return_date IS NULL")
                return [self.map_row(row) for row in cursor.fetchall()]
    
    def return_book(self, loan_id: int, return_date: date) -> Optional[LoanRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    UPDATE library.loan
                    SET return_date = %s
                    WHERE loan_id = %s
                    RETURNING loan_id, book_id, member_id, loan_date, due_date, return_date
                    """,
                    (return_date, loan_id)
                )
                row = cursor.fetchone()
                return self.map_row(row) if row else None
    
    def delete(self, loan_id: int) -> bool:
        with psycopg.connect(self.conn_string) as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    cursor.execute("DELETE FROM library.loan WHERE loan_id = %s RETURNING loan_id", (loan_id,))
                    return cursor.fetchone() is not None

    def create(self, book_id: int, member_id: int, loan_date: date, due_date: date) -> LoanRecord:
        try:
            with psycopg.connect(self.conn_string) as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    cursor.execute(
                        """
                        INSERT INTO library.loan (book_id, member_id, loan_date, due_date)
                        VALUES (%s, %s, %s, %s)
                        RETURNING loan_id, book_id, member_id, loan_date, due_date, return_date
                        """,
                        (book_id, member_id, loan_date, due_date)
                    )
                    return self.map_row(cursor.fetchone())
        except psycopg.errors.ForeignKeyViolation as e:
            raise ValueError(f"book_id {book_id} or member_id {member_id} doesn't exist") from e
                    