"""
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, Generator

from psycopg import Cursor

from assignments.python_sql_assignment_001.db import Database

#https://typing.python.org/en/latest/reference/generics.html

class DAO[IT, RT](ABC):
    """

    """
    #generally this would be through injection
    def __init__(self, database: Database = Database()) -> None:
        self.database = database

    #https://www.psycopg.org/psycopg3/docs/advanced/rows.html
    def get_cursor(self) -> Generator[Cursor[RT], None, None]:
        return self.database.get_connection_cursor(type(RT))

    @abstractmethod
    def get_all(self) -> list[RT]:
        pass

    @abstractmethod
    def get_by_id(self, record_id: IT) -> Optional[IT]:
        pass

    @abstractmethod
    def create(self, record: RT) -> RT:
        pass

    @abstractmethod
    def update(self, record: RT) -> Optional[RT]:
        pass

    @abstractmethod
    def delete(self, record_id: IT) -> Optional[RT]:
        pass