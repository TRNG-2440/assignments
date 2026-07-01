from datetime import date

from db_setup import initialize_db
from genre_dao import GenreDAO
from book_dao import BookDAO
from member_dao import MemberDAO
from loan_dao import LoanDAO


def main():
    initialize_db()

    genre_dao = GenreDAO()
    book_dao = BookDAO()
    member_dao = MemberDAO()
    loan_dao = LoanDAO()

    genre1 = genre_dao.create("Fantasy")
    genre2 = genre_dao.create("Science Fiction")

    member1 = member_dao.create("Alice Smith", "alice@example.com", date(2026, 7, 1))
    member2 = member_dao.create("Bob Jones", "bob@example.com", date(2026, 7, 2))

    book1 = book_dao.create("The Hobbit", "J.R.R. Tolkien", 1937, genre1.genre_id, 3)
    book2 = book_dao.create("Dune", "Frank Herbert", 1965, genre2.genre_id, 5)

    loan1 = loan_dao.create(book1.book_id, member1.member_id, date(2026, 7, 3), date(2026, 7, 17))
    loan2 = loan_dao.create(book2.book_id, member2.member_id, date(2026, 7, 4), date(2026, 7, 18))

    print("All genres:")
    print(genre_dao.get_all())

    print("\nAll books:")
    print(book_dao.get_all())

    print("\nAll members:")
    print(member_dao.get_all())

    print("\nAll loans:")
    print(loan_dao.get_all())

    print("\nOne genre by id:")
    print(genre_dao.get_by_id(genre1.genre_id))

    print("\nUpdated genre:")
    print(genre_dao.update(genre1.genre_id, "Epic Fantasy"))

    print("\nActive loans:")
    print(loan_dao.get_active_loans())

    print("\nReturned loan:")
    print(loan_dao.mark_as_returned(loan1.loan_id, date(2026, 7, 10)))

    print("\nDelete one loan:")
    print(loan_dao.delete(loan2.loan_id))


if __name__ == "__main__":
    main()