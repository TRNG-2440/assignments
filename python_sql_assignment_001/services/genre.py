from dataclasses import asdict
from typing import List, Optional

from psycopg import DatabaseError

from dao.genre_dao import GenreDAO
from models.genre import Genre, GenreCreate, GenreResponse
from exceptions import BooksWithGenreExistsError, GenreExistsError, GenreNotFoundError
from dao.book_dao import BookDAO
from models.book import Book


class GenreService:
    def __init__(self, genre_repo: GenreDAO, book_repo: BookDAO):
        self._genre_repo = genre_repo
        self._book_repo = book_repo

    def get_all(self) -> List[GenreResponse]:
        """
        Retrieve all genres and return them as response models.

        :returns: A list of GenreResponse objects for all genres in the database.
        :rtype: List[GenreResponse]
        """
        genres: List[Genre] = self._genre_repo.get_all()
        return type(self)._convert_to_responses(genres)

    def get_by_id(self, genre_id) -> GenreResponse:
        """
        Retrieve a single genre by its primary key and return it as a response model.

        :param genre_id: The primary key of the genre to fetch.
        :returns: A GenreResponse object for the matching genre.
        :rtype: GenreResponse
        :raises GenreNotFoundError: If no genre record is found for the given ID.
        """
        genre: Optional[Genre] = self._genre_repo.get_by_id(genre_id)
        if not genre:
            raise GenreNotFoundError(genre_id, "No record found!")
        return type(self)._convert_to_response(genre)

    def create(self, create_genre: GenreCreate) -> GenreResponse:
        """
        Create a new genre after validating that it does not already exist.

        :param create_genre: A GenreCreate model containing the name of the genre to create.
        :type create_genre: GenreCreate
        :returns: A GenreResponse object for the newly created genre.
        :rtype: GenreResponse
        :raises GenreExistsError: If a genre with the same name already exists.
        :raises DatabaseError: If the create operation returns no result.
        """
        genres: List[Genre] = self._genre_repo.get_all()
        genre_exists = any(
            genre for genre in genres if genre.genre_name == create_genre.genre_name
        )
        if genre_exists:
            raise GenreExistsError(create_genre.genre_name, "Genre already exists!")
        created_genre: Optional[Genre] = self._genre_repo.create(
            create_genre.genre_name
        )
        if not created_genre:
            raise DatabaseError()
        return type(self)._convert_to_response(created_genre)

    def update(self, genre_id: int, update_genre: GenreCreate) -> GenreResponse:
        """
        Update the name of an existing genre.

        :param genre_id: The primary key of the genre to update.
        :type genre_id: int
        :param update_genre: A GenreCreate model containing the new genre name.
        :type update_genre: GenreCreate
        :returns: A GenreResponse object reflecting the updated genre.
        :rtype: GenreResponse
        :raises GenreNotFoundError: If no genre record is found for the given ID.
        :raises DatabaseError: If the update operation returns no result.
        """
        genre: Optional[Genre] = self._genre_repo.get_by_id(genre_id)
        if not genre:
            raise GenreNotFoundError(genre_id, "No record found!")
        updated_genre = self._genre_repo.update(genre_id, update_genre.genre_name)
        if not updated_genre:
            raise DatabaseError()
        return type(self)._convert_to_response(updated_genre)

    def delete_by_id(self, genre_id: int) -> None:
        """
        Delete a genre by its primary key, provided no books are assigned to it.

        Verifies the genre exists and that no books are currently associated with
        it before proceeding with deletion, preventing orphaned book records.

        :param genre_id: The primary key of the genre to delete.
        :type genre_id: int
        :returns: None
        :raises GenreNotFoundError: If no genre record is found for the given ID.
        :raises BooksWithGenreExistsError: If one or more books are still assigned to this genre.
        """
        genre: Optional[Genre] = self._genre_repo.get_by_id(genre_id)
        if not genre:
            raise GenreNotFoundError(genre_id, "No record found!")
        books: List[Book] = self._book_repo.get_by_genre_id(genre_id)
        if books:
            raise BooksWithGenreExistsError(genre_id, "Books with this genre exist!")
        self._genre_repo.delete(genre_id)

    @classmethod
    def _convert_to_responses(cls, genres: List[Genre]) -> List[GenreResponse]:
        """
        Convert a list of Genre dataclass instances to a list of GenreResponse models.

        :param genres: A list of Genre dataclass instances to convert.
        :type genres: List[Genre]
        :returns: A list of validated GenreResponse objects.
        :rtype: List[GenreResponse]
        """
        return [cls._convert_to_response(genre) for genre in genres]

    @staticmethod
    def _convert_to_response(genre: Genre) -> GenreResponse:
        """
        Convert a single Genre dataclass instance to a GenreResponse model.

        :param genre: The Genre dataclass instance to convert.
        :type genre: Genre
        :returns: A validated GenreResponse object.
        :rtype: GenreResponse
        """
        genre_dict = asdict(genre)
        return GenreResponse.model_validate(genre_dict)
