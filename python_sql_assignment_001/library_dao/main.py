from db import initialize_db
from daos import GenreDAO, BookDAO, MemberDAO, LoanDAO 


def main():
    initialize_db()


    #create genre, book and member DAO objects
    genre_dao = GenreDAO()
    book_dao = BookDAO()
    member_dao = MemberDAO()
    loan_dao = LoanDAO()

    mystery = genre_dao.create("Mystery")
    fiction = genre_dao.create("fiction")


    book1 = book_dao.create(
        "The Alchemist",
        "Paulo Coelho",
        1988,
        fiction["genre_id"],
        5

    )

    book2 = book_dao.create(
        "The Da Vinci Code",
        "Dan Brown",
        2003,
        mystery["genre_id"],
        4
    )

    member1 = member_dao.create(
        "Alex Tran",
        "adtran867@gmail.com",
        "2024-06-05"
    )

    member2 = member_dao.create(
        "John Doe",
        "johdoe123.gmail.com",
        "2026-01-01"
    )

    loan1 = loan_dao.create(
        book1["1"],
        member1["500"],
        "2026-06-10",
        "2026-06-31"
    )

    loan2 = loan_dao.create(
        book1["2"],
        member1["400"],
        "2026-06-05",
        "2026-06-26"
    )


    print("\nAll genres:")
    print(genre_dao.get_all())

    print("\nAll books:")
    print(book_dao.get_all())

    print("\nAll members:")
    print(member_dao.get_all())

    print("\nAll loans:")
    print(loan_dao.get_all())

    print("\nRead one book:")
    print(book_dao.get_by_id(book1["book_id"]))

    print("\nUpdate one genre:")
    print(genre_dao.update(fiction["genre_id"], "Classic Fiction"))

    print("\nReturn one book:")
    print(loan_dao.return_book(loan1["loan_id"], "2026-06-20"))

    print("\nActive loans:")
    print(loan_dao.get_active_loans())

    print("\nDelete one loan:")
    print(loan_dao.delete(loan2["loan_id"]))

    print("\nLoans after delete:")
    print(loan_dao.get_all())


if __name__ == "__main__":
    main()