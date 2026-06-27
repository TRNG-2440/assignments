from pydantic.dataclasses import dataclass

@dataclass
class GenreRecord:
    genre_id: int
    name: str

@dataclass
class BookRecord:
    pass
    #TODO
