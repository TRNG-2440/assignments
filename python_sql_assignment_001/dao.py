from dataclasses import dataclass
from typing import Optional

from db_util import get_connection


@dataclass
class GenreRecord:
    genre_id: int
    name: str


@dataclass
class BookRecord:
    book_id: int
    title: str
    author: str
    publication_year: int
    genre_id: int
    copy_count: int


@dataclass
class MemberRecord:
    member_id: int
    full_name: str
    email: str
    join_date: str


@dataclass
class LoanRecord:
    loan_id: int
    book_id: int
    member_id: int
    loan_date: str
    due_date: str
    return_date: Optional[str]


def map_row(row, record_class):
    if row is None:
        return None

    return record_class(**dict(row))


class GenreDAO:
    def create(self, name: str) -> GenreRecord:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO Genre (name) VALUES (?)",
                (name,)
            )

            genre_id = cursor.lastrowid

            row = conn.execute(
                "SELECT genre_id, name FROM Genre WHERE genre_id = ?",
                (genre_id,)
            ).fetchone()

            return map_row(row, GenreRecord)

    def get_by_id(self, genre_id: int) -> Optional[GenreRecord]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT genre_id, name FROM Genre WHERE genre_id = ?",
                (genre_id,)
            ).fetchone()

            return map_row(row, GenreRecord)

    def get_all(self) -> list[GenreRecord]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT genre_id, name FROM Genre"
            ).fetchall()

            return [map_row(row, GenreRecord) for row in rows]

    def update(self, genre_id: int, name: str) -> Optional[GenreRecord]:
        with get_connection() as conn:
            conn.execute(
                "UPDATE Genre SET name = ? WHERE genre_id = ?",
                (name, genre_id)
            )

            row = conn.execute(
                "SELECT genre_id, name FROM Genre WHERE genre_id = ?",
                (genre_id,)
            ).fetchone()

            return map_row(row, GenreRecord)

    def delete(self, genre_id: int) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM Genre WHERE genre_id = ?",
                (genre_id,)
            )

            return cursor.rowcount > 0


class BookDAO:
    def create(
        self,
        title: str,
        author: str,
        publication_year: int,
        genre_id: int,
        copy_count: int
    ) -> BookRecord:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO Book (title, author, publication_year, genre_id, copy_count)
                VALUES (?, ?, ?, ?, ?)
                """,
                (title, author, publication_year, genre_id, copy_count)
            )

            book_id = cursor.lastrowid

            row = conn.execute(
                """
                SELECT book_id, title, author, publication_year, genre_id, copy_count
                FROM Book
                WHERE book_id = ?
                """,
                (book_id,)
            ).fetchone()

            return map_row(row, BookRecord)

    def get_by_id(self, book_id: int) -> Optional[BookRecord]:
        with get_connection() as conn:
            row = conn.execute(
                """
                SELECT book_id, title, author, publication_year, genre_id, copy_count
                FROM Book
                WHERE book_id = ?
                """,
                (book_id,)
            ).fetchone()

            return map_row(row, BookRecord)

    def get_all(self) -> list[BookRecord]:
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT book_id, title, author, publication_year, genre_id, copy_count
                FROM Book
                """
            ).fetchall()

            return [map_row(row, BookRecord) for row in rows]

    def update(
        self,
        book_id: int,
        title: str,
        author: str,
        publication_year: int,
        genre_id: int,
        copy_count: int
    ) -> Optional[BookRecord]:
        with get_connection() as conn:
            conn.execute(
                """
                UPDATE Book
                SET title = ?, author = ?, publication_year = ?, genre_id = ?, copy_count = ?
                WHERE book_id = ?
                """,
                (title, author, publication_year, genre_id, copy_count, book_id)
            )

            row = conn.execute(
                """
                SELECT book_id, title, author, publication_year, genre_id, copy_count
                FROM Book
                WHERE book_id = ?
                """,
                (book_id,)
            ).fetchone()

            return map_row(row, BookRecord)

    def delete(self, book_id: int) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM Book WHERE book_id = ?",
                (book_id,)
            )

            return cursor.rowcount > 0


class MemberDAO:
    def create(self, full_name: str, email: str, join_date: str) -> MemberRecord:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO Member (full_name, email, join_date)
                VALUES (?, ?, ?)
                """,
                (full_name, email, join_date)
            )

            member_id = cursor.lastrowid

            row = conn.execute(
                """
                SELECT member_id, full_name, email, join_date
                FROM Member
                WHERE member_id = ?
                """,
                (member_id,)
            ).fetchone()

            return map_row(row, MemberRecord)

    def get_by_id(self, member_id: int) -> Optional[MemberRecord]:
        with get_connection() as conn:
            row = conn.execute(
                """
                SELECT member_id, full_name, email, join_date
                FROM Member
                WHERE member_id = ?
                """,
                (member_id,)
            ).fetchone()

            return map_row(row, MemberRecord)

    def get_all(self) -> list[MemberRecord]:
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT member_id, full_name, email, join_date
                FROM Member
                """
            ).fetchall()

            return [map_row(row, MemberRecord) for row in rows]

    def update(
        self,
        member_id: int,
        full_name: str,
        email: str,
        join_date: str
    ) -> Optional[MemberRecord]:
        with get_connection() as conn:
            conn.execute(
                """
                UPDATE Member
                SET full_name = ?, email = ?, join_date = ?
                WHERE member_id = ?
                """,
                (full_name, email, join_date, member_id)
            )

            row = conn.execute(
                """
                SELECT member_id, full_name, email, join_date
                FROM Member
                WHERE member_id = ?
                """,
                (member_id,)
            ).fetchone()

            return map_row(row, MemberRecord)

    def delete(self, member_id: int) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM Member WHERE member_id = ?",
                (member_id,)
            )

            return cursor.rowcount > 0


class LoanDAO:
    def create(
        self,
        book_id: int,
        member_id: int,
        loan_date: str,
        due_date: str
    ) -> LoanRecord:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO Loan (book_id, member_id, loan_date, due_date, return_date)
                VALUES (?, ?, ?, ?, NULL)
                """,
                (book_id, member_id, loan_date, due_date)
            )

            loan_id = cursor.lastrowid

            row = conn.execute(
                """
                SELECT loan_id, book_id, member_id, loan_date, due_date, return_date
                FROM Loan
                WHERE loan_id = ?
                """,
                (loan_id,)
            ).fetchone()

            return map_row(row, LoanRecord)

    def get_by_id(self, loan_id: int) -> Optional[LoanRecord]:
        with get_connection() as conn:
            row = conn.execute(
                """
                SELECT loan_id, book_id, member_id, loan_date, due_date, return_date
                FROM Loan
                WHERE loan_id = ?
                """,
                (loan_id,)
            ).fetchone()

            return map_row(row, LoanRecord)

    def get_all(self) -> list[LoanRecord]:
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT loan_id, book_id, member_id, loan_date, due_date, return_date
                FROM Loan
                """
            ).fetchall()

            return [map_row(row, LoanRecord) for row in rows]

    def get_active_loans(self) -> list[LoanRecord]:
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT loan_id, book_id, member_id, loan_date, due_date, return_date
                FROM Loan
                WHERE return_date IS NULL
                """
            ).fetchall()

            return [map_row(row, LoanRecord) for row in rows]

    def return_book(self, loan_id: int, return_date: str) -> Optional[LoanRecord]:
        with get_connection() as conn:
            conn.execute(
                "UPDATE Loan SET return_date = ? WHERE loan_id = ?",
                (return_date, loan_id)
            )

            row = conn.execute(
                """
                SELECT loan_id, book_id, member_id, loan_date, due_date, return_date
                FROM Loan
                WHERE loan_id = ?
                """,
                (loan_id,)
            ).fetchone()

            return map_row(row, LoanRecord)

    def delete(self, loan_id: int) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM Loan WHERE loan_id = ?",
                (loan_id,)
            )

            return cursor.rowcount > 0