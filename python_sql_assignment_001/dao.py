import psycopg
from psycopg.rows import dict_row
from datetime import date
from dataclasses import dataclass
from db_util import connection_details
from pydantic import Field


@dataclass
class GenreRecord:
    genre_id: int
    genre_name: str

@dataclass
class BookRecord:
    book_id: int
    genre_id: int
    title: str
    author: str
    publication_year: int
    inventory: int

@dataclass
class MemberRecord:
    member_id: int
    member_name: str
    email: str
    date_joined: date

@dataclass
class LoanRecord:
    loan_id: int
    book_id: int
    member_id: int
    date_loaned: date
    date_due: date
    date_returned: date

class GenreDAO:
    def __init__(self):
        self.conn_string = connection_details()
    
    def _convert_row(self, row) -> GenreRecord:
        """convert row to GenreRecord"""
        return GenreRecord(
            genre_id = row["genre_id"],
            genre_name = row["genre_name"]
        )

    def create(self, rec: GenreRecord) -> GenreRecord:
        """create new record in genre table"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    INSERT INTO lfields001.Genre (genre_name)
                    VALUES (%s)
                    RETURNING genre_id
                    """,
                    (rec.genre_name,)
                )
                id = cur.fetchone()["genre_id"]
                return GenreRecord(
                    genre_id = id,
                    genre_name = rec.genre_name
                )

    def get_all(self) -> list:
        """get list of all records from genre table"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("""
                    SELECT genre_id, genre_name FROM lfields001.Genre
                """)

                return [self._convert_row(row) for row in cur.fetchall()]
    
    def get_by_id(self, id: int) -> GenreRecord:
        """get genre by id"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    SELECT genre_id, genre_name FROM lfields001.Genre
                    WHERE genre_id = %s
                    """,
                    (id,)
                )
                r = cur.fetchone()
                return self._convert_row(r) if r else None
    
    def update(self, rec: GenreRecord) -> GenreRecord:
        """update genre name by id"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    UPDATE lfields001.Genre
                    SET genre_name = %s
                    WHERE genre_id = %s
                    RETURNING genre_id, genre_name
                    """,
                    (rec.genre_name, rec.genre_id)
                )
                r = cur.fetchone()
                return self._convert_row(r) if r else None
    
    def delete(self, genre_id: int) -> bool:
        """delete genre by id"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    DELETE FROM lfields001.Genre g WHERE g.genre_id = %s
                    RETURNING g.genre_id
                    """,
                    (genre_id,)
                )
                return cur.fetchone() is not None
            
class BookDAO:
    def __init__(self):
        self.conn_string = connection_details()
    
    def _convert_row(self, row) -> BookRecord:
        """convert row to BookRecord"""
        return BookRecord(
            book_id = row["book_id"],
            genre_id = row["genre_id"],
            title = row["title"],
            author = row["author"],
            publication_year = row["publication_year"],
            inventory = row["inventory"]
        )

    def create(self, rec: BookRecord) -> BookRecord:
        """create new record in book table"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    INSERT INTO lfields001.Book (genre_id, title, author, publication_year, inventory)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING book_id
                    """,
                    (rec.genre_id, rec.title, rec.author, rec.publication_year, rec.inventory)
                )
                id = cur.fetchone()["book_id"]
                return BookRecord(
                    book_id = id,
                    genre_id = rec.genre_id,
                    title = rec.title,
                    author = rec.author,
                    publication_year = rec.publication_year,
                    inventory = rec.inventory
                )

    def get_all(self) -> list:
        """get list of all records from Book table"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("""
                    SELECT book_id, genre_id, title, author, publication_year, inventory
                    FROM lfields001.Book
                """)

                return [self._convert_row(row) for row in cur.fetchall()]
    
    def get_by_id(self, id: int) -> BookRecord:
        """get genre by id"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    SELECT book_id, genre_id, title, author, publication_year, inventory FROM lfields001.Book
                    WHERE book_id = %s
                    """,
                    (id,)
                )
                r = cur.fetchone()
                return self._convert_row(r) if r else None
    
    def update(self, rec: BookRecord) -> BookRecord:
        """update book by id"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    UPDATE lfields001.Book
                    SET genre_id = %s, title = %s, author = %s, publication_year = %s, inventory = %s
                    WHERE book_id = %s
                    RETURNING book_id, genre_id, title, author, publication_year, inventory
                    """,
                    (rec.genre_id, rec.title, rec.author, rec.publication_year, rec.inventory, rec.book_id)
                )
                r = cur.fetchone()
                return self._convert_row(r) if r else None
    
    def delete(self, book_id: int) -> bool:
        """delete book by id"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    DELETE FROM lfields001.Book g WHERE g.book_id = %s
                    RETURNING g.book_id
                    """,
                    (book_id,)
                )
                return cur.fetchone() is not None

class MemberDAO:
    def __init__(self):
        self.conn_string = connection_details()
    
    def _convert_row(self, row) -> MemberRecord:
        """convert row to MemberRecord"""
        return MemberRecord(
            member_id = row["member_id"],
            member_name = row["member_name"],
            email = row["email"],
            date_joined = row["date_joined"]
        )

    def create(self, rec: MemberRecord) -> MemberRecord:
        """create new record in book table"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    INSERT INTO lfields001.Member (member_name, email, date_joined)
                    VALUES (%s, %s, %s)
                    RETURNING member_id
                    """,
                    (rec.member_name, rec.email, rec.date_joined)
                )
                id = cur.fetchone()["member_id"]
                return MemberRecord(
                    member_id = id,
                    member_name = rec.member_name,
                    email = rec.email,
                    date_joined = rec.date_joined
                )

    def get_all(self) -> list:
        """get list of all records from Member table"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    SELECT m.member_id, m.member_name, m.email, m.date_joined
                    FROM lfields001.Member m
                    """
                )
                return [self._convert_row(row) for row in cur.fetchall()]
    
    def get_by_id(self, id: int) -> MemberRecord:
        """get member record by id"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    SELECT m.member_id, m.member_name, m.email, m.date_joined FROM lfields001.Member m
                    WHERE m.member_id = %s
                    """,
                    (id,)
                )
                r = cur.fetchone()
                return self._convert_row(r) if r else None
    
    def update(self, rec: MemberRecord) -> MemberRecord:
        """update genre name by id"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    UPDATE lfields001.Member m
                    SET m.member_name = %s, m.email = %s, m.date_joined = %s
                    WHERE m.member_id = %s
                    RETURNING m.member_id, m.member_name, m.email, m.date_joined
                    """,
                    (rec.member_name, rec.email, rec.date_joined, rec.member_id)
                )
                r = cur.fetchone()
                return self._convert_row(r) if r else None
    
    def delete(self, member_id: int) -> bool:
        """delete member by id"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    DELETE FROM lfields001.Member m WHERE m.member_id = %s
                    RETURNING m.member_id
                    """,
                    (member_id,)
                )
                return cur.fetchone() is not None

class LoanDAO:
    def __init__(self):
        self.conn_string = connection_details()
    
    def _convert_row(self, row) -> LoanRecord:
        """convert row to LoanRecord"""
        return LoanRecord(
            loan_id = row["loan_id"],
            book_id = row["book_id"],
            member_id = row["member_id"],
            date_loaned = row["date_loaned"],
            date_due = row["date_due"],
            date_returned = row["date_returned"]
        )

    def create(self, rec: LoanRecord) -> LoanRecord:
        """create new record in Loan table"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    INSERT INTO lfields001.Loan (book_id, member_id, date_loaned, date_due, date_returned)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING loan_id
                    """,
                    (rec.book_id, rec.member_id, rec.date_loaned, rec.date_due, rec.date_returned)
                )
                id = cur.fetchone()["loan_id"]
                return LoanRecord(
                    loan_id = id,
                    book_id = rec.book_id,
                    member_id = rec.member_id,
                    date_loaned = rec.date_loaned,
                    date_due = rec.date_due,
                    date_returned = rec.date_returned
                )

    def get_all(self) -> list:
        """get list of all records from Loan table"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    SELECT l.loan_id, l.book_id, l.member_id, l.date_loaned, l.date_due, l.date_returned
                    FROM lfields001.Loan l
                    """
                )
                return [self._convert_row(row) for row in cur.fetchall()]
    
    def get_by_id(self, id: int) -> LoanRecord:
        """get loan record by id"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    SELECT l.loan_id, l.book_id, l.member_id, l.date_loaned, l.date_due, l.date_returned
                    FROM lfields001.Loan l
                    WHERE l.loan_id = %s
                    """,
                    (id,)
                )
                r = cur.fetchone()
                return self._convert_row(r) if r else None

    def update(self, rec: LoanRecord) -> LoanRecord:
        """update loan record by id"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    UPDATE lfields001.Loan l
                    SET l.book_id = %s, l.member_id = %s, l.date_loaned = %s, l.date_due = %s, l.date_returned = %s
                    WHERE l.loan_id = %s
                    RETURNING l.loan_id, l.book_id, l.member_id, l.date_loaned, l.date_due, l.date_returned
                    """,
                    (rec.book_id, rec.member_id, rec.date_loaned, rec.date_due, rec.date_returned, rec.loan_id)
                )
                r = cur.fetchone()
                return self._convert_row(r) if r else None
    
    def delete(self, loan_id: int) -> bool:
        """delete laon by id"""
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    DELETE FROM lfields001.Loan l WHERE l.loan_id = %s
                    RETURNING l.loan_id
                    """,
                    (loan_id,)
                )
                return cur.fetchone() is not None