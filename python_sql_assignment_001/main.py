from dotenv import load_dotenv

from logger import logger
from dao.genre_dao import GenreDAO
from db.database import DatabaseManager

load_dotenv()


def main():
    # Initialize database
    db_manager = DatabaseManager()

    # Insert records into Genre table
    genre = GenreDAO()
    inserted_genre = genre.create("Action")
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

    # Close db connection
    db_manager.close_all()


if __name__ == "__main__":
    main()
