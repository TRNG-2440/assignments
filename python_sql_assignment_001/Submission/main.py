from postgresCrudDAO import genericDao
from GenreDAO import GenreDAO
from BookDAO import BookDAO
from MemberDAO import MemberDAO
from LoanDAO import LoanDAO


def main():
    host = "localhost"
    port = 5432
    database = "library"
    user = "postgres"      # TODO: implement from ENV, or Fill in yourself before executing
    password = "password"  # TODO: implement from ENV, or Fill in yourself before executing

    conn_string = (
        f"postgresql://{user}:{password}@{host}:{port}/{database}"
    )

    dao = genericDao(conn_string)

    genre_dao = GenreDAO(dao)
    book_dao = BookDAO(dao)
    member_dao = MemberDAO(dao)
    loan_dao = LoanDAO(dao)

    # Inserting Genres
    print("Inserting")
    fiction = genre_dao.create("Fiction")
    fantasy = genre_dao.create("Fantasy")

    print(fiction)
    print(fantasy)
    print()

    # Inserting books
    book1 = book_dao.create( "1984", "George Orwell", 1949, fiction[0], 5 )
    book2 = book_dao.create( "The Cat in the Hat", "Dr. Seuss", 1957, fantasy[0], 3 )

    print(book1)
    print(book2)
    print()

    # Insert member
    member1 = member_dao.create( "Theodore Roosevelt", "teddy.roosevelt@example.com", "1901-09-14")
    member2 = member_dao.create( "John Fitzgerald Kennedy", "jfk@example.com", "1961-01-20")

    print(member1)
    print(member2)
    print()

    # Insert loans
    loan1 = loan_dao.create( book1[0], member1[0], "2026-01-01", "2026-01-15")
    loan2 = loan_dao.create( book1[0], member1[0], "2026-01-02", "2026-01-16")

    print(loan1)
    print(loan2)
    print()

    # Get all Genres
    print("Genre Get all")
    print(genre_dao.get_all())
    print()

    # Update Genres
    print("Upgrade Genres")
    updated_genre = genre_dao.update(fiction[0], "Literary Fiction")
    print(updated_genre)
    print()

    # Get all books
    print("Get all books")
    print(book_dao.get_all())
    print()

    # Update Books
    print("Update Books")
    updated_book = book_dao.update(
        book1[0],
        "Nineteen Eighty-Four",
        "George Orwell",
        1949,
        fiction[0],
        10
    )
    print(updated_book)
    print()

    # Delete a book
    print("Delete a book")
    book_dao.delete(book2[0])
    print()

    # Get all books (should only return one)
    print("Get all books")
    print(book_dao.get_all())
    print()

    # Get all members
    print("Get all members")
    print(member_dao.get_all())
    print()

    # Update members
    print("Update Members")
    updated_member = member_dao.update(
        member1[0],
        "Theodore Roosevelt Jr.",
        "teddy.roosevelt@example.com",
        "1901-09-14"
    )
    print(updated_member)
    print()

    # Delete members
    print("Delete members")
    member_dao.delete(member2[0])
    print()

    # Get all Members
    print("Get all members")
    print(member_dao.get_all())
    print()

    # Get active loans
    print("Get active loans")
    print(loan_dao.get_active_loans())
    print()

    # Return book
    print("Return a book")
    returned = loan_dao.return_book(
        loan1[0],
        "2026-01-10"
    )
    print(returned)
    print()

    # Delete Loan
    print("Delete a loan")
    loan_dao.delete(loan2[0])
    print()

    # Get all Loans
    print("Get all loans")
    print(loan_dao.get_all())
    print()

if __name__ == "__main__":
    main()