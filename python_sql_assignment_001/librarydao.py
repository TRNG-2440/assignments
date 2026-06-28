"""
"""
from abc import ABC, abstractmethod
from contextlib import _GeneratorContextManager
from typing import Optional

from psycopg import Cursor, ProgrammingError

from assignments.python_sql_assignment_001.db import Database
from assignments.python_sql_assignment_001.records import GenreRecord


#https://typing.python.org/en/latest/reference/generics.html

class Dao[IT, RT](ABC):
    """

    """

    #generally this would be through injection
    def __init__(self, row_type: type[RT], database: Database = Database()) -> None:
        self.database = database
        self._row_type = row_type

    #https://www.psycopg.org/psycopg3/docs/advanced/rows.html
    def get_cursor(self) -> _GeneratorContextManager[Cursor[RT], None, None]:
        return self.database.get_connection_cursor(self._row_type)

    @abstractmethod
    def get_all(self) -> list[RT]:
        pass

    @abstractmethod
    def get_by_id(self, record_id: IT) -> Optional[IT]:
        pass

    @abstractmethod
    def create(self, record: Optional[RT] = None, **kwargs) -> RT:
        pass

    @abstractmethod
    def update(self, record: Optional[RT] = None, **kwargs) -> Optional[RT]:
        pass

    @abstractmethod
    def delete(self, record_id: IT) -> Optional[RT]:
        pass


class GenreDao(Dao[int, GenreRecord]):

    def __init__(self, database: Database = Database()) -> None:
        super().__init__(GenreRecord, database)

    def get_all(self) -> list[GenreRecord]:
        with self.get_cursor() as cursor:
            query: str = """
                SELECT genre_id, name FROM Genre;
            """
            cursor.execute(query)
            return cursor.fetchall()

    def get_by_id(self, record_id: int) -> Optional[GenreRecord]:
        with self.get_cursor() as cursor:
            query: str = """
                SELECT genre_id, name FROM Genre
                WHERE genre_id = %s
            """
            cursor.execute(query, (record_id,))
            try:
                return cursor.fetchone()
            except ProgrammingError:
                return None

    def create(self, record: Optional[GenreRecord] = None, name: str = "") -> GenreRecord:
        if record is None:
            record = GenreRecord(genre_id=-1, name=name)
        with self.get_cursor() as cursor:
            update: str = """
            INSERT INTO Genre (genre_id, name) VALUES (DEFAULT, %s)
            ON CONFLICT DO NOTHING
            RETURNING genre_id, name
            """
            cursor.execute(update, (record.name,))
            return next(cursor)

    def update(self, record: Optional[GenreRecord] = None, genre_id: int = -1, name: str = "") -> Optional[GenreRecord]:
        """

        :param record:
        :param genre_id: if record is None
        :param name: if record is None
        """
        if record is None:
            record = GenreRecord(genre_id=genre_id, name=name)
        with self.get_cursor() as cursor:
            update: str = """
            UPDATE Genre
            SET name = %s
            WHERE genre_id = %s
            RETURNING genre_id, name
            """
            cursor.execute(update, (record.name, record.genre_id))
            try:
                return cursor.fetchone()
            except ProgrammingError:
                return None

    def delete(self, record_id: int) -> Optional[GenreRecord]:
        with self.get_cursor() as cursor:
            delete: str = """
            DELETE FROM Genre
            WHERE genre_id = %s
            """
            cursor.execute(delete, (record_id,))
            try:
                return cursor.fetchone()
            except ProgrammingError:
                return None
