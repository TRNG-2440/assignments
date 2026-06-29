from datetime import date
from typing import List, Optional
from psycopg.rows import class_row

from db.database import DatabaseManager
from model import Book, Loan
from logger import logger
from dao.book_dao import BookDAO


class LoanDAO:
    def __init__(self, db_manager: DatabaseManager, book_dao: BookDAO):
        self._db_manager = db_manager
        self._book_dao = book_dao

    def create(
        self,
        book_id: int,
        member_id: int,
        loan_date: date,
        due_date: date,
        return_date: Optional[date] = None,
    ) -> Loan:
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Loan)) as cur:
                    if not return_date:
                        loan_book: Book = self._book_dao.get_by_id(book_id)
                        updated_book = self._book_dao.update_available_copies(
                            book_id, loan_book.available_copies - 1
                        )
                        logger.info(f"Updated book details: {updated_book}")
                    query = """INSERT INTO loan(book_id, member_id, loan_date, due_date, return_date) 
                        VALUES(%s, %s, %s, %s, %s) 
                        RETURNING loan_id, book_id, member_id, loan_date, due_date, return_date"""
                    result = cur.execute(
                        query, (book_id, member_id, loan_date, due_date, return_date)
                    ).fetchone()

                    if not result:
                        logger.error(
                            f"Error encountered while creating new loan record for {member_id} borrowing {book_id}!"
                        )
                        raise ValueError("Error encountered on db operation!")
                    return result

    def get_by_id(self, loan_id) -> Loan:
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Loan)) as cur:
                    query = """SELECT loan_id, book_id, member_id, loan_date, due_date, return_date
                        FROM loan WHERE loan_id = %s"""
                    result = cur.execute(query, (loan_id,)).fetchone()

                    if not result:
                        logger.error(f"No record found for loan_id: {loan_id}")
                        raise ValueError("Error encountered on db operation!")
                    return result

    def get_all(self) -> List[Loan]:
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Loan)) as cur:
                    query = """SELECT loan_id, book_id, member_id, loan_date, due_date, return_date
                        FROM loan"""
                    result = cur.execute(query).fetchall()

                    if not result:
                        logger.error("No records found!")
                        raise ValueError("Error encountered on db operation!")
                    return result

    def get_active_loans(self) -> List[Loan]:
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Loan)) as cur:
                    query = """SELECT loan_id, book_id, member_id, loan_date, due_date, return_date
                        FROM loan WHERE return_date is NULL"""
                    result = cur.execute(query).fetchall()
                    return result

    def return_book(self, loan_id: int, return_date: date) -> Loan:
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Loan)) as cur:
                    loan_record: Loan = self.get_by_id(loan_id)
                    return_book: Book = self._book_dao.get_by_id(loan_record.book_id)
                    updated_book = self._book_dao.update_available_copies(
                        loan_record.book_id, return_book.available_copies + 1
                    )
                    logger.info(f"Updated book details: {updated_book}")

                    query = """UPDATE loan 
                                SET return_date = %s
                                WHERE loan_id = %s 
                                RETURNING loan_id, book_id, member_id, loan_date, due_date, return_date"""
                    result = cur.execute(
                        query,
                        (return_date, loan_id),
                    ).fetchone()

                    if not result:
                        logger.error(
                            f"Error encountered while updating loan_id: {loan_id}!"
                        )
                        raise ValueError("Error encountered on db operation!")
                    return result

    def delete(self, loan_id) -> None:
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    query = "DELETE FROM loan WHERE loan_id = %s"
                    cur.execute(query, (loan_id,))

                    if cur.rowcount == 0:
                        logger.error(f"No record found for loan_id: {loan_id}")
                        raise ValueError("Error encountered on db operation!")
