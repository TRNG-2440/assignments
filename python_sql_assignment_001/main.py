from datetime import date

from dotenv import load_dotenv

from logger import logger
from dao.genre_dao import GenreDAO
from db.database import DatabaseManager
from dao.book_dao import BookDAO
from dao.member_dao import MemberDAO
from dao.loan_dao import LoanDAO

load_dotenv()


def main():
    # Initialize database
    db_manager = DatabaseManager()

    # Insert records into Genre table
    genre = GenreDAO(db_manager)
    inserted_genre = genre.create("Mystery")
    logger.info(f"Inserted genre: {inserted_genre}")

    inserted_genre = genre.create("Romance")
    logger.info(f"Inserted genre: {inserted_genre}")

    inserted_genre = genre.create("Fantasy")
    logger.info(f"Inserted genre: {inserted_genre}")

    # Get record by id
    selected_genre = genre.get_by_id(1)
    logger.info(f"Fetched genre: {selected_genre}")

    # Update record
    updated_genre = genre.update(3, "Comedy")
    logger.info(f"Updated genre_id: 3 to {updated_genre}")

    # Delete record
    genre.delete(3)
    logger.info("Deleted record with genre_id: 3")

    # Get all records
    genres = genre.get_all()
    logger.info(f"Fetched records: {genres}")

    # Insert records for Book table
    book = BookDAO(db_manager)
    inserted_book = book.create(
        title="The Devotion of Suspect X",
        author="Higashino Keigo",
        publication_year="2005",
        genre_id=1,
        copy_count=3,
    )
    logger.info(f"Inserted book: {inserted_book}")

    inserted_book = book.create(
        title="The Rosie Project",
        author="Graeme Simsion",
        publication_year="2013",
        genre_id=2,
        copy_count=1,
    )
    logger.info(f"Inserted book: {inserted_book}")

    inserted_book = book.create(
        title="And Then There Were None",
        author="Agatha Christie",
        publication_year="1939",
        genre_id=1,
        copy_count=2,
    )
    logger.info(f"Inserted book: {inserted_book}")

    # Get record by id
    selected_book = book.get_by_id(1)
    logger.info(f"Fetched book: {selected_book}")

    # Update record
    updated_book = book.update(
        3,
        title="Murder on the Orient Express",
        author="Agatha Christie",
        publication_year="1934",
        genre_id=1,
        copy_count=2,
    )
    logger.info(f"Updated book_id: 3 to {updated_book}")

    # Delete record
    book.delete(3)
    logger.info("Deleted record with book_id: 3")

    # Get all records
    books = book.get_all()
    logger.info(f"Fetched records: {books}")

    # Insert records for Member table
    member = MemberDAO(db_manager)
    inserted_member = member.create(
        "Tom Cruise", "tomcruz@email.com", date(2010, 9, 22)
    )
    logger.info(f"Inserted member: {inserted_member}")

    inserted_member = member.create(
        "Elizabeth Benett", "lizbenett@email.com", date(1945, 3, 12)
    )
    logger.info(f"Inserted member: {inserted_member}")

    inserted_member = member.create("John Doe", "johndoe@email.com", date(2022, 7, 12))
    logger.info(f"Inserted member: {inserted_member}")

    # Get record by id
    selected_member = member.get_by_id(1)
    logger.info(f"Fetched member: {selected_member}")

    # Update record
    updated_member = member.update(
        3, "Indiana Jones", "indyjones@email.com", date(2001, 3, 30)
    )
    logger.info(f"Updated member_id: 3 to {updated_member}")

    # Delete record
    member.delete(3)
    logger.info("Deleted record with member_id: 3")

    # Get all records
    members = member.get_all()
    logger.info(f"Fetched records: {members}")

    # Insert records for Loan table
    loan = LoanDAO(db_manager, book)
    inserted_loan = loan.create(
        1, 1, date(2026, 6, 15), date(2026, 6, 22), date(2026, 6, 20)
    )
    logger.info(f"Inserted loan: {inserted_loan}")

    inserted_loan = loan.create(1, 2, date(2026, 6, 22), date(2026, 6, 29))
    logger.info(f"Inserted loan: {inserted_loan}")

    inserted_loan = loan.create(2, 1, date(2026, 6, 24), date(2026, 7, 1))
    logger.info(f"Inserted loan: {inserted_loan}")

    # Get record by id
    selected_loan = loan.get_by_id(1)
    logger.info(f"Fetched loan: {selected_loan}")

    active_loans = loan.get_active_loans()
    logger.info(f"Fetched active loans : {active_loans}")

    # Update record
    returned_loan = loan.return_book(2, date(2026, 6, 28))
    logger.info(f"Returned loan: {returned_loan}")

    # Delete record
    loan.delete(2)
    logger.info("Deleted record with loan_id: 2")

    # Get all records
    loans = loan.get_all()
    logger.info(f"Fetched records: {loans}")

    # Close db connection
    db_manager.close_all()


if __name__ == "__main__":
    main()
