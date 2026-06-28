from datetime import date

from librarydao import GenreDao, BookDao, MemberDao, LoanDao
from records import GenreRecord, BookRecord, Member, Loan
from db import Database

if __name__ == "__main__":
    database: Database = Database()
    #create the tables
    with database.get_connection() as conn, open("create_tables.sql", "r") as ct:
        conn.execute(ct.read())
        #clear the tables (if they already existed)
        conn.execute("""
            TRUNCATE Genre CASCADE;
            TRUNCATE Book CASCADE;
            TRUNCATE Member CASCADE;
            TRUNCATE Loan CASCADE;
        """)

    genre_dao: GenreDao = GenreDao(database)

    fantasy_genre: GenreRecord = genre_dao.create(name="Fantasy")
    science_fiction_genre: GenreRecord = genre_dao.create(record=GenreRecord(genre_id=1, name="Science Fiction"))

    print("Genre Dao")
    print("Create Fantasy -", fantasy_genre)
    print("Create Science Fiction -", science_fiction_genre)

    print("Get All -", genre_dao.get_all())
    print("Genre Fantasy -", genre_dao.get_by_id(fantasy_genre.genre_id))
    print("Delete Fantasy -", genre_dao.delete(fantasy_genre.genre_id))
    print("Genre Fantasy (will be None) -", genre_dao.get_by_id(fantasy_genre.genre_id))
    print("Get All -", genre_dao.get_all())

    print("Update Science Fiction to Sci-Fi -", genre_dao.update(genre_id=science_fiction_genre.genre_id, name="Sci-Fi"))
    print("Get Science Fiction -", genre_dao.get_by_id(science_fiction_genre.genre_id))
    #re-add fantasy-genre
    fantasy_genre: GenreRecord = genre_dao.create(name="Fantasy")

    # Book
    book_dao: BookDao = BookDao(database)

    dune: BookRecord = book_dao.create(title="Dune", author="Frank Herbert", publication_year=date(1965, 8, 1), genre_id=science_fiction_genre.genre_id, copy_count=5)
    hobbit: BookRecord = book_dao.create(record=BookRecord(book_id=-1, title="The Hobbit", author="J.R.R. Tolkien", publication_year=date(1937, 9, 21), genre_id=fantasy_genre.genre_id, copy_count=3))
    
    print("Book Dao")
    print("Create Dune -", dune)
    print("Create The Hobbit -", hobbit)

    print("Get All Books -", book_dao.get_all())
    print("Get Dune -", book_dao.get_by_id(dune.book_id))
    print("Delete Dune -", book_dao.delete(dune.book_id))
    print("Get Dune (will be None) -", book_dao.get_by_id(dune.book_id))
    print("Get All Books -", book_dao.get_all())

    print("Update The Hobbit copy_count to 10 -", book_dao.update(book_id=hobbit.book_id, title=hobbit.title, author=hobbit.author, publication_year=hobbit.publication_year, genre_id=hobbit.genre_id, copy_count=10))
    print("Get The Hobbit -", book_dao.get_by_id(hobbit.book_id))

    # Member
    member_dao: MemberDao = MemberDao(database)

    alice: Member = member_dao.create(name="Alice Smith", email="alice@example.com", join_date=date(2024, 1, 15))
    bob: Member = member_dao.create(record=Member(member_id=-1, name="Bob Smith", email="bob@example.com", join_date=date(2024, 3, 10)))

    print("Member Dao")
    print("Create Alice -", alice)
    print("Create Bob -", bob)

    print("Get All Members -", member_dao.get_all())
    print("Get Alice -", member_dao.get_by_id(alice.member_id))
    print("Delete Alice -", member_dao.delete(alice.member_id))
    print("Get Alice (will be None) -", member_dao.get_by_id(alice.member_id))
    print("Get All Members -", member_dao.get_all())

    print("Update Bob's email -", member_dao.update(member_id=bob.member_id, name=bob.name, email="bob.smith@example.com", join_date=bob.join_date))
    print("Get Bob -", member_dao.get_by_id(bob.member_id))
    #re-add alice
    alice: Member = member_dao.create(name="Alice Smith", email="alice@example.com", join_date=date(2024, 1, 15))

    # Loan
    loan_dao: LoanDao = LoanDao(database)

    loan1: Loan = loan_dao.create(book_id=hobbit.book_id, member_id=bob.member_id, loan_date=date(2024, 6, 1), due_date=date(2024, 6, 15))
    loan2: Loan = loan_dao.create(record=Loan(loan_id=-1, book_id=hobbit.book_id, member_id=bob.member_id, loan_date=date(2024, 7, 1), due_date=date(2024, 7, 15), return_date=date(2024, 7, 10)))

    print("Loan Dao")
    print("Create Loan 1 -", loan1)
    print("Create Loan 2 (already returned) -", loan2)

    print("Get All Loans -", loan_dao.get_all())
    print("Get Loan 1 -", loan_dao.get_by_id(loan1.loan_id))
    print("Delete Loan 1 -", loan_dao.delete(loan1.loan_id))
    print("Get Loan 1 (will be None) -", loan_dao.get_by_id(loan1.loan_id))
    print("Get All Loans -", loan_dao.get_all())

    print("Return Loan 2 -", loan_dao.update(loan_id=loan2.loan_id, book_id=loan2.book_id, member_id=loan2.member_id, loan_date=loan2.loan_date, due_date=loan2.due_date, return_date=date(2024, 7, 10)))
    print("Get Loan 2 -", loan_dao.get_by_id(loan2.loan_id))

