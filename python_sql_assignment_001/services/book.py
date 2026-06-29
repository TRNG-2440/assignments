from dataclasses import asdict
from typing import List, Optional

from psycopg import DatabaseError

from models.book import Book, BookCreate, BookResponse
from exceptions import BookIsLoanedError, BookNotFoundError, GenreNotFoundError
from models.genre import Genre
from models.model import Loan


class BookService:
    def __init__(self, book_repo, genre_repo, loan_repo) -> None:
        self._book_repo = book_repo
        self._genre_repo = genre_repo
        self._loan_repo = loan_repo

    def get_all(self) -> List[BookResponse]:
        """
        Retrieve all books and return them as response models.

        :returns: A list of BookResponse objects for all books in the database.
        :rtype: List[BookResponse]
        """
        books: List[Book] = self._book_repo.get_all()
        return type(self)._convert_to_responses(books)

    def get_by_id(self, book_id) -> BookResponse:
        """
        Retrieve a single book by its primary key and return it as a response model.

        :param book_id: The primary key of the book to fetch.
        :returns: A BookResponse object for the matching book.
        :rtype: BookResponse
        :raises BookNotFoundError: If no book record is found for the given ID.
        """
        book: Optional[Book] = self._book_repo.get_by_id(book_id)
        if not book:
            raise BookNotFoundError(book_id, "No record found!")
        return type(self)._convert_to_response(book)

    def create(self, create_book: BookCreate) -> BookResponse:
        """
        Create a new book after validating that its genre exists.

        :param create_book: A BookCreate model containing the new book's details.
        :type create_book: BookCreate
        :returns: A BookResponse object for the newly created book.
        :rtype: BookResponse
        :raises GenreNotFoundError: If no genre record is found for the given genre ID.
        :raises DatabaseError: If the create operation returns no result.
        """
        genre: Genre = self._genre_repo.get_by_id(create_book.genre_id)
        if not genre:
            raise GenreNotFoundError(create_book.genre_id, "Genre not found!")
        created_book: Optional[Book] = self._book_repo.create(
            create_book.title,
            create_book.author_name,
            create_book.publication_year,
            create_book.genre_id,
            create_book.total_copies,
        )
        if not created_book:
            raise DatabaseError()
        return type(self)._convert_to_response(created_book)

    def update(self, book_id: int, update_book: BookCreate) -> BookResponse:
        """
        Update all fields of an existing book record.

        :param book_id: The primary key of the book to update.
        :type book_id: int
        :param update_book: A BookCreate model containing the updated book details.
        :type update_book: BookCreate
        :returns: A BookResponse object reflecting the updated book.
        :rtype: BookResponse
        :raises BookNotFoundError: If no book record is found for the given ID.
        :raises DatabaseError: If the update operation returns no result.
        """
        book: Optional[Book] = self._book_repo.get_by_id(book_id)
        if not book:
            raise BookNotFoundError(book_id, "No record found!")
        updated_book = self._book_repo.update(
            book_id,
            update_book.title,
            update_book.author_name,
            update_book.publication_year,
            update_book.genre_id,
            update_book.total_copies,
        )
        if not updated_book:
            raise DatabaseError()
        return type(self)._convert_to_response(updated_book)

    def delete_by_id(self, book_id: int) -> None:
        """
        Delete a book by its primary key, provided it is not currently on loan.

        Verifies the book exists and has no active loans before proceeding.
        If safe to delete, its full loan history is cleared first to avoid
        orphaned loan records, then the book itself is removed.

        :param book_id: The primary key of the book to delete.
        :type book_id: int
        :returns: None
        :raises BookNotFoundError: If no book record is found for the given ID.
        :raises BookIsLoanedError: If the book currently has an active loan with no return date.
        """
        book: Optional[Book] = self._book_repo.get_by_id(book_id)
        if not book:
            raise BookNotFoundError(book_id, "No record found!")
        loans: List[Loan] = self._loan_repo.get_active_loans()
        book_loan_exists = any(
            loan
            for loan in loans
            if loan.book_id == book_id and loan.return_date is None
        )
        if book_loan_exists:
            raise BookIsLoanedError(book_id, "This book has been borrowed!")
        self._loan_repo.delete_book_loan_history(book_id)
        self._book_repo.delete(book_id)

    @classmethod
    def _convert_to_responses(cls, books: List[Book]) -> List[BookResponse]:
        """
        Convert a list of Book dataclass instances to a list of BookResponse models.

        :param books: A list of Book dataclass instances to convert.
        :type books: List[Book]
        :returns: A list of validated BookResponse objects.
        :rtype: List[BookResponse]
        """
        return [cls._convert_to_response(book) for book in books]

    @staticmethod
    def _convert_to_response(book: Book) -> BookResponse:
        """
        Convert a single Book dataclass instance to a BookResponse model.

        :param book: The Book dataclass instance to convert.
        :type book: Book
        :returns: A validated BookResponse object.
        :rtype: BookResponse
        """
        book_dict = asdict(book)
        return BookResponse.model_validate(book_dict)
