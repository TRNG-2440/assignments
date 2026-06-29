from datetime import date, timedelta

from db_util import initialize_db
from dao import GenreDAO, BookDAO, MemberDAO, LoanDAO


def main():
    initialize_db()

    genre_dao = GenreDAO()
    book_dao = BookDAO()
    member_dao = MemberDAO()
    loan_dao = LoanDAO()

    today = date.today()
    due_date_one = today + timedelta(days=14)
    due_date_two = today + timedelta(days=21)

    fiction = genre_dao.create("Fiction")
    mystery = genre_dao.create("Mystery")

    book_one = book_dao.create(
        "1984",
        "George Orwell",
        1949,
        fiction.genre_id,
        4
    )

    book_two = book_dao.create(
        "The Hound of the Baskervilles",
        "Arthur Conan Doyle",
        1902,
        mystery.genre_id,
        2
    )

    member_one = member_dao.create(
        "Alice Johnson",
        "alice@example.com",
        today.isoformat()
    )

    member_two = member_dao.create(
        "Brian Smith",
        "brian@example.com",
        today.isoformat()
    )

    loan_one = loan_dao.create(
        book_one.book_id,
        member_one.member_id,
        today.isoformat(),
        due_date_one.isoformat()
    )

    loan_two = loan_dao.create(
        book_two.book_id,
        member_two.member_id,
        today.isoformat(),
        due_date_two.isoformat()
    )

    print("All genres:")
    print(genre_dao.get_all())

    print("All books:")
    print(book_dao.get_all())

    print("All members:")
    print(member_dao.get_all())

    print("All loans:")
    print(loan_dao.get_all())

    print("Read one book:")
    print(book_dao.get_by_id(book_one.book_id))

    print("Update one book:")
    updated_book = book_dao.update(
        book_one.book_id,
        "Nineteen Eighty-Four",
        "George Orwell",
        1949,
        fiction.genre_id,
        5
    )
    print(updated_book)

    print("Return one book:")
    returned_loan = loan_dao.return_book(
        loan_one.loan_id,
        today.isoformat()
    )
    print(returned_loan)

    print("Active loans:")
    print(loan_dao.get_active_loans())

    print("Delete one loan:")
    deleted = loan_dao.delete(loan_two.loan_id)
    print(deleted)


if __name__ == "__main__":
    main()