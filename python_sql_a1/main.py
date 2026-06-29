from db import initialize_db
from DAO import GenreDAO, BookDAO, MemberDAO, LoanDAO

def main():
    initialize_db()

    genre_1 = GenreDAO.create("Fiction")
    genre_2 = GenreDAO.create("Science Fiction")

    book1 = BookDAO.create("Little Women", "Louisa May Alcott", 1868, genre_1['genre_id'], 1)
    book2 = BookDAO.create("1984", "George Orwell", 1949, genre_2['genre_id'], 3)

    member_1 = MemberDAO.create("John Doe", "john@doe.com", "2026-01-15")
    member_2 = MemberDAO.create("Jane Doe", "jane@doe.com", "2026-03-22")

    l1 = LoanDAO.create(book1['book_id'], member_1['member_id'], "2026-06-20", "2026-07-04")
    l2 = LoanDAO.create(book2['book_id'], member_2['member_id'], "2026-06-25", "2026-07-09")

    active_loans = LoanDAO.get_active_loans()
    
    updated_book = BookDAO.update(book1['book_id'], book1['title'], book1['author'], book1['publication_year'], book1['genre_id'], 10)

    returned_loan = LoanDAO.return_book(l1['loan_id'], "2026-06-27")

    MemberDAO.delete(member_2['member_id'])

if __name__ == "__main__":
    main()