import psycopg
from psycopg.rows import dict_row
from typing import Optional
from datetime import date

from db_util import get_conn_string
from dao import LoanRecord


class LoanDAO:
    def __init__(self):
        self.conn_string = get_conn_string()

    def _map_row(self, row) -> LoanRecord:
        return LoanRecord(
            loan_id=row["loan_id"],
            book_id=row["book_id"],
            member_id=row["member_id"],
            loan_date=row["loan_date"],
            due_date=row["due_date"],
            return_date=row["return_date"]
        )

    def create(
        self,
        book_id: int,
        member_id: int,
        loan_date: date,
        due_date: date,
        return_date: Optional[date] = None
    ) -> LoanRecord:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    INSERT INTO library.loans (
                        book_id,
                        member_id,
                        loan_date,
                        due_date,
                        return_date
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING loan_id, book_id, member_id, loan_date, due_date, return_date
                """, (book_id, member_id, loan_date, due_date, return_date))
                row = cursor.fetchone()
                return self._map_row(row)

    def get_by_id(self, loan_id: int) -> Optional[LoanRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    SELECT loan_id, book_id, member_id, loan_date, due_date, return_date
                    FROM library.loans
                    WHERE loan_id = %s
                """, (loan_id,))
                row = cursor.fetchone()
                return self._map_row(row) if row else None

    def get_all(self) -> list[LoanRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    SELECT loan_id, book_id, member_id, loan_date, due_date, return_date
                    FROM library.loans
                    ORDER BY loan_id
                """)
                rows = cursor.fetchall()
                return [self._map_row(row) for row in rows]

    def update(
        self,
        loan_id: int,
        book_id: int,
        member_id: int,
        loan_date: date,
        due_date: date,
        return_date: Optional[date]
    ) -> Optional[LoanRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    UPDATE library.loans
                    SET book_id = %s,
                        member_id = %s,
                        loan_date = %s,
                        due_date = %s,
                        return_date = %s
                    WHERE loan_id = %s
                    RETURNING loan_id, book_id, member_id, loan_date, due_date, return_date
                """, (
                    book_id,
                    member_id,
                    loan_date,
                    due_date,
                    return_date,
                    loan_id
                ))
                row = cursor.fetchone()
                return self._map_row(row) if row else None

    def delete(self, loan_id: int) -> bool:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    DELETE FROM library.loans
                    WHERE loan_id = %s
                    RETURNING loan_id
                """, (loan_id,))
                return cursor.fetchone() is not None

    def get_active_loans(self) -> list[LoanRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    SELECT loan_id, book_id, member_id, loan_date, due_date, return_date
                    FROM library.loans
                    WHERE return_date IS NULL
                    ORDER BY loan_id
                """)
                rows = cursor.fetchall()
                return [self._map_row(row) for row in rows]

    def mark_as_returned(self, loan_id: int, return_date: date) -> Optional[LoanRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    UPDATE library.loans
                    SET return_date = %s
                    WHERE loan_id = %s
                    RETURNING loan_id, book_id, member_id, loan_date, due_date, return_date
                """, (return_date, loan_id))
                row = cursor.fetchone()
                return self._map_row(row) if row else None