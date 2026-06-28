"""
"""
from abc import ABC, abstractmethod
from contextlib import _GeneratorContextManager
from datetime import date
from typing import Optional

from psycopg import Cursor, ProgrammingError

from db import Database
from records import GenreRecord, BookRecord, Member, Loan


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
            RETURNING genre_id, name
            """
            cursor.execute(delete, (record_id,))
            try:
                return cursor.fetchone()
            except ProgrammingError:
                return None


class BookDao(Dao[int, BookRecord]):

    def __init__(self, database: Database = Database()) -> None:
        super().__init__(BookRecord, database)

    def get_all(self) -> list[BookRecord]:
        with self.get_cursor() as cursor:
            query: str = """
                SELECT book_id, title, author, publication_year, genre_id, copy_count FROM Book;
            """
            cursor.execute(query)
            return cursor.fetchall()

    def get_by_id(self, record_id: int) -> Optional[BookRecord]:
        with self.get_cursor() as cursor:
            query: str = """
                SELECT book_id, title, author, publication_year, genre_id, copy_count FROM Book
                WHERE book_id = %s
            """
            cursor.execute(query, (record_id,))
            try:
                return cursor.fetchone()
            except ProgrammingError:
                return None

    def create(self, record: Optional[BookRecord] = None,
               title: str = "",
               author: str = "",
               publication_year: date = date.min,
               genre_id: int = -1,
               copy_count: int = 0,
               ) -> BookRecord:
        if record is None:
            record = BookRecord(book_id=-1, title=title, author=author, publication_year=publication_year, genre_id=genre_id, copy_count=copy_count)
        with self.get_cursor() as cursor:
            insert: str = """
            INSERT INTO Book (book_id, title, author, publication_year, genre_id, copy_count)
            VALUES (DEFAULT, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            RETURNING book_id, title, author, publication_year, genre_id, copy_count
            """
            cursor.execute(insert, (record.title, record.author, record.publication_year, record.genre_id, record.copy_count))
            return next(cursor)

    def update(self, record: Optional[BookRecord] = None,
               book_id: int = -1,
               title: str = "",
               author: str = "",
               publication_year: date = date.min,
               genre_id: int = -1,
               copy_count: int = 0,
               ) -> Optional[BookRecord]:
        """

        :param record:
        :param book_id: if record is None
        :param title: if record is None
        :param author: if record is None
        :param publication_year: if record is None
        :param genre_id: if record is None
        :param copy_count: if record is None
        """
        if record is None:
            record = BookRecord(book_id=book_id, title=title, author=author, publication_year=publication_year, genre_id=genre_id, copy_count=copy_count)
        with self.get_cursor() as cursor:
            update: str = """
            UPDATE Book
            SET title = %s, author = %s, publication_year = %s, genre_id = %s, copy_count = %s
            WHERE book_id = %s
            RETURNING book_id, title, author, publication_year, genre_id, copy_count
            """
            cursor.execute(update, (record.title, record.author, record.publication_year, record.genre_id, record.copy_count, record.book_id))
            try:
                return cursor.fetchone()
            except ProgrammingError:
                return None

    def delete(self, record_id: int) -> Optional[BookRecord]:
        with self.get_cursor() as cursor:
            delete: str = """
            DELETE FROM Book
            WHERE book_id = %s
            RETURNING book_id, title, author, publication_year, genre_id, copy_count
            """
            cursor.execute(delete, (record_id,))
            try:
                return cursor.fetchone()
            except ProgrammingError:
                return None


class MemberDao(Dao[int, Member]):

    def __init__(self, database: Database = Database()) -> None:
        super().__init__(Member, database)

    def get_all(self) -> list[Member]:
        with self.get_cursor() as cursor:
            query: str = """
                SELECT member_id, name, email, join_date FROM Member;
            """
            cursor.execute(query)
            return cursor.fetchall()

    def get_by_id(self, record_id: int) -> Optional[Member]:
        with self.get_cursor() as cursor:
            query: str = """
                SELECT member_id, name, email, join_date FROM Member
                WHERE member_id = %s
            """
            cursor.execute(query, (record_id,))
            try:
                return cursor.fetchone()
            except ProgrammingError:
                return None

    def create(self, record: Optional[Member] = None,
               name: str = "",
               email: str = "",
               join_date: date = date.today(),
               ) -> Member:
        if record is None:
            record = Member(member_id=-1, name=name, email=email, join_date=join_date)
        with self.get_cursor() as cursor:
            insert: str = """
            INSERT INTO Member (member_id, name, email, join_date)
            VALUES (DEFAULT, %s, %s, %s)
            ON CONFLICT DO NOTHING
            RETURNING member_id, name, email, join_date
            """
            cursor.execute(insert, (record.name, record.email, record.join_date))
            return next(cursor)

    def update(self, record: Optional[Member] = None,
               member_id: int = -1,
               name: str = "",
               email: str = "",
               join_date: date = date.min,
               ) -> Optional[Member]:
        """

        :param record:
        :param member_id: if record is None
        :param name: if record is None
        :param email: if record is None
        :param join_date: if record is None
        """
        if record is None:
            record = Member(member_id=member_id, name=name, email=email, join_date=join_date)
        with self.get_cursor() as cursor:
            update: str = """
            UPDATE Member
            SET name = %s, email = %s, join_date = %s
            WHERE member_id = %s
            RETURNING member_id, name, email, join_date
            """
            cursor.execute(update, (record.name, record.email, record.join_date, record.member_id))
            try:
                return cursor.fetchone()
            except ProgrammingError:
                return None

    def delete(self, record_id: int) -> Optional[Member]:
        with self.get_cursor() as cursor:
            delete: str = """
            DELETE FROM Member
            WHERE member_id = %s
            RETURNING member_id, name, email, join_date
            """
            cursor.execute(delete, (record_id,))
            try:
                return cursor.fetchone()
            except ProgrammingError:
                return None


class LoanDao(Dao[int, Loan]):

    def __init__(self, database: Database = Database()) -> None:
        super().__init__(Loan, database)

    def get_all(self) -> list[Loan]:
        with self.get_cursor() as cursor:
            query: str = """
                SELECT loan_id, book_id, member_id, loan_date, due_date, return_date FROM Loan;
            """
            cursor.execute(query)
            return cursor.fetchall()

    def get_by_id(self, record_id: int) -> Optional[Loan]:
        with self.get_cursor() as cursor:
            query: str = """
                SELECT loan_id, book_id, member_id, loan_date, due_date, return_date FROM Loan
                WHERE loan_id = %s
            """
            cursor.execute(query, (record_id,))
            try:
                return cursor.fetchone()
            except ProgrammingError:
                return None

    def create(self, record: Optional[Loan] = None,
               book_id: int = -1,
               member_id: int = -1,
               loan_date: date = date.today(),
               due_date: date = date.today(),
               return_date: Optional[date] = None,
               ) -> Loan:
        if record is None:
            record = Loan(loan_id=-1, book_id=book_id, member_id=member_id, loan_date=loan_date, due_date=due_date, return_date=return_date)
        with self.get_cursor() as cursor:
            insert: str = """
            INSERT INTO Loan (loan_id, book_id, member_id, loan_date, due_date, return_date)
            VALUES (DEFAULT, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            RETURNING loan_id, book_id, member_id, loan_date, due_date, return_date
            """
            cursor.execute(insert, (record.book_id, record.member_id, record.loan_date, record.due_date, record.return_date))
            return next(cursor)

    def update(self, record: Optional[Loan] = None,
               loan_id: int = -1,
               book_id: int = -1,
               member_id: int = -1,
               loan_date: date = date.min,
               due_date: date = date.min,
               return_date: Optional[date] = None,
               ) -> Optional[Loan]:
        """

        :param record:
        :param loan_id: if record is None
        :param book_id: if record is None
        :param member_id: if record is None
        :param loan_date: if record is None
        :param due_date: if record is None
        :param return_date: if record is None
        """
        if record is None:
            record = Loan(loan_id=loan_id, book_id=book_id, member_id=member_id, loan_date=loan_date, due_date=due_date, return_date=return_date)
        with self.get_cursor() as cursor:
            update: str = """
            UPDATE Loan
            SET book_id = %s, member_id = %s, loan_date = %s, due_date = %s, return_date = %s
            WHERE loan_id = %s
            RETURNING loan_id, book_id, member_id, loan_date, due_date, return_date
            """
            cursor.execute(update, (record.book_id, record.member_id, record.loan_date, record.due_date, record.return_date, record.loan_id))
            try:
                return cursor.fetchone()
            except ProgrammingError:
                return None

    def delete(self, record_id: int) -> Optional[Loan]:
        with self.get_cursor() as cursor:
            delete: str = """
            DELETE FROM Loan
            WHERE loan_id = %s
            RETURNING loan_id, book_id, member_id, loan_date, due_date, return_date
            """
            cursor.execute(delete, (record_id,))
            try:
                return cursor.fetchone()
            except ProgrammingError:
                return None