class GenreNotFoundError(Exception):
    def __init__(self, genre_id, detail) -> None:
        self.genre_id = genre_id
        self.detail = detail


class MemberNotFoundError(Exception):
    def __init__(self, member_id, detail) -> None:
        self.member_id = member_id
        self.detail = detail


class BookNotFoundError(Exception):
    def __init__(self, book_id, detail) -> None:
        self.book_id = book_id
        self.detail = detail


class LoanNotFoundError(Exception):
    def __init__(self, loan_id, detail) -> None:
        self.loan_id = loan_id
        self.detail = detail


class GenreExistsError(Exception):
    def __init__(self, genre_name, detail) -> None:
        self.genre_name = genre_name
        self.detail = detail


class MemberExistsError(Exception):
    def __init__(self, member_email, detail) -> None:
        self.member_email = member_email
        self.detail = detail


class BooksWithGenreExistsError(Exception):
    def __init__(self, genre_id, detail) -> None:
        self.genre_id = genre_id
        self.detail = detail


class MemberHasLoansError(Exception):
    def __init__(self, member_id, detail) -> None:
        self.member_id = member_id
        self.detail = detail


class BookIsLoanedError(Exception):
    def __init__(self, book_id, detail) -> None:
        self.book_id = book_id
        self.detail = detail


class NoAvailableCopiesError(Exception):
    def __init__(self, book_id, detail) -> None:
        self.book_id = book_id
        self.detail = detail


class ActiveLoanError(Exception):
    def __init__(self, loan_id, detail) -> None:
        self.loan_id = loan_id
        self.detail = detail
