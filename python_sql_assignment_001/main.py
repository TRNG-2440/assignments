from datetime import date
from dao import GenreDAO, BookDAO, MemberDAO, LoanDAO
from initialize_db import initialize_db


def main():
    initialize_db()

    genre_dao = GenreDAO()
    book_dao = BookDAO()
    member_dao = MemberDAO()
    loan_dao = LoanDAO()

    # genres
    fiction = genre_dao.create("Fiction")
    sci_fi = genre_dao.create("Sci-fi")

    # books
    book1 = book_dao.create("Piranesi", "Susanna Clark", 2020, fiction.genre_id, 3)
    book2 = book_dao.create("WOOL", "Hugh Howey", 2011, sci_fi.genre_id, 2)

    # members
    will = member_dao.create("William Mahnke", "wm@gmail.com", date(2024, 5, 4))
    bob = member_dao.create("Bob Reader", "bob@gmail.com", date.today())

    # loans
    loan1 = loan_dao.create(book1.book_id, will.member_id, date(2024, 5, 4), date(2024, 6, 4))
    loan2 = loan_dao.create(book2.book_id, bob.member_id, date.today(), date(2024, 6, 21))

    # READ
    print("All books:", book_dao.get_all())

    # UPDATE
    updated = genre_dao.update(sci_fi.genre_id, "Mystery")
    print("Updated genre:", updated)

    # DELETE
    deleted = loan_dao.delete(loan2.loan_id)
    print("Deleted loan2?", deleted)
    print("Active loans:", loan_dao.get_active_loans())


if __name__ == "__main__":
    main()
