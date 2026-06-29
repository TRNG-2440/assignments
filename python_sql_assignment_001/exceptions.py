class GenreNotFoundError(Exception):
    def __init__(self, genre_id, detail) -> None:
        self.genre_id = genre_id
        self.detail = detail


class GenreExistsError(Exception):
    def __init__(self, genre_name, detail) -> None:
        self.genre_name = genre_name
        self.detail = detail


class BooksWithGenreExistsError(Exception):
    def __init__(self, genre_id, detail) -> None:
        self.genre_id = genre_id
        self.detail = detail
