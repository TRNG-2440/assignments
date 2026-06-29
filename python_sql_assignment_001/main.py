# #Mark White
# 2026/06/28
#Library management system


from datetime import date

from src.dao.genre_dao import GenreDAO
from src.dao.book_dao import BookDAO
from src.dao.member_dao import MemberDAO
from src.dao.loan_dao import LoanDAO

def main():
    genre_dao = GenreDAO()
    book_dao = BookDAO()
    member_dao = MemberDAO()
    loan_dao = LoanDAO()



    # CREATE GENRE
    fiction = genre_dao.create("Fantasy")
    dystopian = genre_dao.create("Dystopian")

    # CREATE BOOK
    book1 = book_dao.create(
        "Harry Potter and the Sorcerer's Stone",
        "J.K. Rowling",
        1997,
        fiction["genre_id"],
        10
    )
    print("Book created:", book1)

    book2 = book_dao.create(
        "The Hunger Games",
        "Suzanne Collins",
        2008,
        dystopian["genre_id"],
        7
    )
    print("Book created:", book2)

    
    # CREATE MEMBERS
    member = member_dao.create(
        "Alice Anderson",
        "AlAnderson@example.com",
        "2026-01-01"
    )
    print("Member created:", member)

    member2 = member_dao.create(
        "Bobby Brown",
        "BobbyB@example.com",
        "2026-02-01"
    )
    print("Member created:", member2)


    # CREATE LOAN
    loan = loan_dao.create(
        book1["book_id"],
        member["member_id"],
        "2026-06-26",
        "2026-07-26"
    )
    print("Loan created:", loan)

    loan2 = loan_dao.create(
        book2["book_id"],
        member2["member_id"],
        "2026-06-26",
        "2026-07-26"
    )
    print("Loan created:", loan2)

   
    # READ DATA
    print("\nAll Books:")
    print(book_dao.get_all())

    print("\nActive Loans:")
    print(loan_dao.get_active_loans())

  
    # RETURN BOOK
    returned = loan_dao.return_book(
        loan["loan_id"],
        returned_date=date.today()
    )
    print("\nBook returned:", returned)


    # DELETE LOAN/MEMBER/BOOK/GENRE
    deleted = loan_dao.delete(loan["loan_id"])
    print("\nLoan deleted:", deleted)

    deleted = member_dao.delete(member["member_id"])
    print("\nMember deleted:", deleted)

    deleted = book_dao.delete(book1["book_id"])
    print("\nBook deleted:", deleted)

    deleted = genre_dao.delete(fiction["genre_id"])
    print("\nGenre deleted:", deleted)


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        print("\nERROR:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {e}")

    finally:
        print("\n Execution complete.")