from datetime import date, timedelta

from dao import BookDAO, GenreDAO, LoanDAO, MemberDAO
from database import Create_Database


def main() -> None:
    # Initialize the database and create tables from schema.sql
    Create_Database()

    # Instantiate each DAO object
    genreDao = GenreDAO()
    bookDao = BookDAO()
    membersDao = MemberDAO()
    loanDao = LoanDAO()

    # Call functions from genreDoa
    fiction = genreDao.create("Fiction")
    philosophy = genreDao.create("Philosphy")
    
    # Call functions from bookDao
    book1 = bookDao.create("48 Laws of Power", "Robert Greene", 2000, philosophy.genre_id, 31 )
    book2 = bookDao.create("The Kite Runner", "Khaled Hosseini", 2003, fiction.genre_id, 20)

    # Call functions from membersDao
    member1 = membersDao.create("Kyle Drewes", "kdrewes@example.com", date(2026, 6, 28))
    member2 = membersDao.create("Brianne Drewes", "bdrewes@example.com", date(2023, 1, 20))

    # Call functions from loanDao
    today = date.today()
    loan1 = loanDao.create(book1.book_id, member1.member_id, today, today + timedelta(days=14))
    loan2 = loanDao.create(book2.book_id, member2.member_id, today, today + timedelta(days=14) )

    # Display all genres
    print("All genres:", genreDao.get_all())
    print("Book ID:", bookDao.get_by_id(book1.book_id))
    print("Loans:", loanDao.get_active_loans())

    # Perform an update operation on genreDao member function
    genreDao.update(philosophy.genre_id, "Modern philosophy")
    print("Updated genre:", genreDao.get_by_id(fiction.genre_id))

    # Perform loan operation on loadDao object       
    loanDao.return_book(loan1.loan_id, today + timedelta(days=7))
    print("Returned loan:", loanDao.get_by_id(loan1.loan_id))

     # Perform delete operation on loadDao object
    loanDao.delete(loan2.loan_id)
    print("Remaining loans:", loanDao.get_all())

if __name__ == "__main__":
    main()