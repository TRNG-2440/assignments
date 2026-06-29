from dataclasses import asdict
from datetime import datetime
from typing import List, Optional

from psycopg import DatabaseError
from models.loan import Loan, LoanCreate, LoanResponse
from exceptions import (
    ActiveLoanError,
    BookNotFoundError,
    LoanNotFoundError,
    NoAvailableCopiesError,
)
from models.book import Book


class LoanService:
    def __init__(self, loan_repo, book_repo) -> None:
        self._loan_repo = loan_repo
        self._book_repo = book_repo

    def get_all(self) -> List[LoanResponse]:
        """
        Retrieve all loans and return them as response models.

        :returns: A list of LoanResponse objects for all loans in the database.
        :rtype: List[LoanResponse]
        """
        loans: List[Loan] = self._loan_repo.get_all()
        return type(self)._convert_to_responses(loans)

    def get_active_loans(self) -> List[LoanResponse]:
        """
        Retrieve all loans that have not yet been returned and return them as response models.

        :returns: A list of LoanResponse objects for all active loans, or an empty list if none exist.
        :rtype: List[LoanResponse]
        """
        loans: List[Loan] = self._loan_repo.get_active_loans()
        return type(self)._convert_to_responses(loans)

    def get_by_id(self, loan_id) -> LoanResponse:
        """
        Retrieve a single loan by its primary key and return it as a response model.

        :param loan_id: The primary key of the loan to fetch.
        :returns: A LoanResponse object for the matching loan.
        :rtype: LoanResponse
        :raises LoanNotFoundError: If no loan record is found for the given ID.
        """
        loan: Optional[Loan] = self._loan_repo.get_by_id(loan_id)
        if not loan:
            raise LoanNotFoundError(loan_id, "No record found!")
        return type(self)._convert_to_response(loan)

    def create(self, loan: LoanCreate) -> LoanResponse:
        """
        Create a new loan after verifying the book has at least one available copy.

        :param loan: A LoanCreate model containing the loan details.
        :type loan: LoanCreate
        :returns: A LoanResponse object for the newly created loan.
        :rtype: LoanResponse
        :raises NoAvailableCopiesError: If the book has no available copies to loan out.
        :raises DatabaseError: If the create operation returns no result.
        """
        book_to_loan: Book = self._book_repo.has_available_copies(loan.book_id)
        if not book_to_loan:
            raise NoAvailableCopiesError(loan.book_id, "No copies available to borrow!")
        created_loan = self._loan_repo.create(
            loan.book_id,
            loan.member_id,
            loan.loan_date,
            loan.due_date,
            loan.return_date,
        )
        if not created_loan:
            raise DatabaseError
        return type(self)._convert_to_response(created_loan)

    def return_book(self, loan_id: int) -> LoanResponse:
        """
        Process a book return by closing the loan and incrementing the book's available copy count.

        Fetches the loan and its associated book, then delegates the return
        and copy count update to the loan repository.

        :param loan_id: The primary key of the loan to close.
        :type loan_id: int
        :returns: A LoanResponse object reflecting the closed loan with its return date populated.
        :rtype: LoanResponse
        :raises LoanNotFoundError: If no loan record is found for the given ID.
        :raises BookNotFoundError: If the book associated with the loan cannot be found.
        """
        loan_record: Optional[Loan] = self._loan_repo.get_by_id(loan_id)
        if not loan_record:
            raise LoanNotFoundError(loan_id, "No record found!")
        loan_book: Optional[Book] = self._book_repo.get_by_id(loan_record.book_id)
        if not loan_book:
            raise BookNotFoundError(loan_record.book_id, "Book not found!")
        cleared_loan = self._loan_repo.return_book(
            loan_id, loan_record.book_id, loan_book.available_copies
        )
        return type(self)._convert_to_response(cleared_loan)

    def delete_by_id(self, loan_id) -> None:
        """
        Delete a loan by its primary key, provided it is not currently active.

        Verifies the loan exists and has a return date before proceeding,
        preventing deletion of loans that are still open.

        :param loan_id: The primary key of the loan to delete.
        :returns: None
        :raises LoanNotFoundError: If no loan record is found for the given ID.
        :raises ActiveLoanError: If the loan has no return date, indicating it is still active.
        """
        loan: Optional[Loan] = self._loan_repo.get_by_id(loan_id)
        if not loan:
            raise LoanNotFoundError(loan_id, "No record found!")
        if not loan.return_date:
            raise ActiveLoanError(loan_id, "The loan is currently active!")
        self._loan_repo.delete(loan_id)

    @classmethod
    def _convert_to_responses(cls, loans: List[Loan]) -> List[LoanResponse]:
        """
        Convert a list of Loan dataclass instances to a list of LoanResponse models.

        :param loans: A list of Loan dataclass instances to convert.
        :type loans: List[Loan]
        :returns: A list of validated LoanResponse objects.
        :rtype: List[LoanResponse]
        """
        return [cls._convert_to_response(loan) for loan in loans]

    @staticmethod
    def _convert_to_response(loan: Loan) -> LoanResponse:
        """
        Convert a single Loan dataclass instance to a LoanResponse model.

        :param loan: The Loan dataclass instance to convert.
        :type loan: Loan
        :returns: A validated LoanResponse object.
        :rtype: LoanResponse
        """
        loan_dict = asdict(loan)
        return LoanResponse.model_validate(loan_dict)
