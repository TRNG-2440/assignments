from datetime import date
from typing import List, Optional
from psycopg.rows import class_row

from db.database import DatabaseManager
from models.model import Loan
from models.book import Book
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
        """
        Insert a new loan record into the database.

        If no return_date is provided, the book's available copy count is
        decremented by 1 before the loan record is inserted, reflecting that
        the book is now on loan.

        :param book_id: The primary key of the book being loaned.
        :type book_id: int
        :param member_id: The primary key of the member borrowing the book.
        :type member_id: int
        :param loan_date: The date the book was loaned out.
        :type loan_date: date
        :param due_date: The date by which the book must be returned.
        :type due_date: date
        :param return_date: The date the book was returned, or None if still on loan.
        :type return_date: Optional[date]
        :returns: The newly created Loan object with its assigned ID and all fields.
        :rtype: Loan
        :raises ValueError: If the insert operation returns no result.
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Loan)) as cur:
                    if not return_date:
                        loan_book: Optional[Book] = self._book_dao.get_by_id(book_id)
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
        """
        Retrieve a single loan record by its primary key.

        :param loan_id: The primary key of the loan to fetch.
        :returns: The Loan object matching the given ID.
        :rtype: Loan
        :raises ValueError: If no loan record is found for the given ID.
        """
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
        """
        Retrieve all loan records from the database, including both active and returned loans.

        :returns: A list of all Loan objects stored in the loan table.
        :rtype: List[Loan]
        :raises ValueError: If no loan records are found or the table is empty.
        """
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
        """
        Retrieve all loan records where the book has not yet been returned.

        Active loans are identified by a NULL return_date. Unlike other read
        methods, an empty result is not treated as an error, as having no
        active loans is a valid state.

        :returns: A list of active Loan objects, or an empty list if none exist.
        :rtype: List[Loan]
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Loan)) as cur:
                    query = """SELECT loan_id, book_id, member_id, loan_date, due_date, return_date
                        FROM loan WHERE return_date is NULL"""
                    result = cur.execute(query).fetchall()
                    return result

    def return_book(self, loan_id: int, return_date: date) -> Loan:
        """
        Record a book return by setting the return_date on an existing loan.

        Fetches the loan and its associated book, increments the book's available
        copy count by 1, then updates the loan record with the provided return date.

        :param loan_id: The primary key of the loan being closed.
        :type loan_id: int
        :param return_date: The date the book was returned.
        :type return_date: date
        :returns: The updated Loan object with the return_date populated.
        :rtype: Loan
        :raises ValueError: If the loan record is not found, or if the update
            operation returns no result.
        """
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
        """
        Delete a loan record from the database by its primary key.

        Permanently removes the row from the loan table. A ValueError is
        raised if the given ID does not match any existing record, detected
        by checking the cursor's rowcount after execution.

        :param loan_id: The primary key of the loan to delete.
        :returns: None
        :raises ValueError: If no loan record is found for the given ID.
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    query = "DELETE FROM loan WHERE loan_id = %s"
                    cur.execute(query, (loan_id,))

                    if cur.rowcount == 0:
                        logger.error(f"No record found for loan_id: {loan_id}")
                        raise ValueError("Error encountered on db operation!")

    def get_by_member_id(self, member_id) -> List[Loan]:
        """
        Retrieve all loan records associated with a specific member.

        Unlike other read methods, an empty result is not treated as an error,
        as having no loans under a given member is a valid state.

        :param member_id: The foreign key of the member to filter loans by.
        :returns: A list of Loan objects matching the given member, or an empty list if none exist.
        :rtype: List[Loan]
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Loan)) as cur:
                    query = """SELECT loan_id, book_id, member_id, loan_date, due_date, return_date
                        FROM loan WHERE member_id = %s"""
                    result = cur.execute(query, (member_id,)).fetchall()
                    return result

    def delete_book_loan_history(self, book_id) -> None:
        """
        Delete all completed loan records associated with a specific book.

        Only removes loans where a return_date is present, preserving any
        active loans. Intended to be called prior to deleting a book record
        to avoid orphaned loan history.

        :param book_id: The foreign key of the book whose loan history should be cleared.
        :returns: None
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    query = "DELETE FROM loan WHERE book_id = %s AND return_date IS NOT NULL"
                    cur.execute(query, (book_id,))
