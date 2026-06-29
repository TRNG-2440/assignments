from datetime import date
from typing import Optional

from database import Connection
from models import Book, Genre, Loan, Member

# Genre class
class GenreDAO:

    # Converts a DB dictionary (dictionary which contains criteria from a row) into a data class
    def MapRow(self, row: dict) -> Genre:
        return Genre(genre_id=row["genre_id"], name=row["genre_name"])

    # Create genre - add into database table
    def create(self, name: str) -> Genre:
        with Connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "INSERT INTO Genre (genre_name) VALUES (%s)",
                    (name,),
                )
                genre_id = cursor.lastrowid
            conn.commit()
        return self.get_by_id(genre_id)

    # Retrieve a single genre by ID
    def get_by_id(self, genre_id: int) -> Optional[Genre]:
        with Connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "SELECT genre_id, genre_name FROM Genre WHERE genre_id = %s",
                    (genre_id,),
                )
                row = cursor.fetchone()
                return self.MapRow(row) if row else None

    # Retrieve all genres
    def get_all(self) -> list[Genre]:
        with Connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "SELECT genre_id, genre_name FROM Genre ORDER BY genre_id"
                )
                return [self.MapRow(row) for row in cursor.fetchall()]

    # Update genre table
    def update(self, genre_id: int, name: str) -> Optional[Genre]:
        with Connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE Genre SET genre_name = %s WHERE genre_id = %s",
                    (name, genre_id),
                )
            conn.commit()
        return self.get_by_id(genre_id)

    # Delete row from genre table
    def delete(self, genre_id: int) -> None:
        with Connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute
                (
                    "DELETE FROM Genre WHERE genre_id = %s",
                    (genre_id,),
                )
            conn.commit()

# Books class
class BookDAO:

    # Converts a DB dictionary into a Book data class
    def MapRow(self, row: dict) -> Book:
        return Book(
            book_id=row["book_id"],
            title=row["title"],
            author=row["author"],
            publication_year=row["publication_year"],
            genre_id=row["genre_id"],
            copy_count=row["copy_count"],
        )

    # Create book - add into database table
    def create(
        self,
        title: str,
        author: str,
        publication_year: int,
        genre_id: int,
        copy_count: int,
    ) -> Book:
        with Connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute
                (
                    "INSERT INTO Book (title, author, publication_year, genre_id, copy_count) VALUES (%s, %s, %s, %s, %s)",
                    (title, author, publication_year, genre_id, copy_count),
                )
                book_id = cursor.lastrowid
            conn.commit()
        return self.get_by_id(book_id)

    # Retrieve a single book by ID
    def get_by_id(self, book_id: int) -> Optional[Book]:
        with Connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute
                (
                    "SELECT book_id, title, author, publication_year, genre_id, copy_count FROM Book WHERE book_id = %s",
                    (book_id,),
                )

                # Fetch single row
                row = cursor.fetchone()

                return self.MapRow(row) if row else None

    # Retrieve all books
    def get_all(self) -> list[Book]:
        with Connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT book_id, title, author, publication_year, genre_id, copy_count FROM Book ORDER BY book_id")
                return [self.MapRow(row) for row in cursor.fetchall()]

    # Update book table
    def update(self, book_id: int, title: str, author: str, publication_year: int, genre_id: int, copy_count: int,) -> Optional[Book]:
        with Connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Book SET title = %s, author = %s, publication_year = %s,genre_id = %s, copy_count = %s WHERE book_id = %s",
                    (title, author, publication_year, genre_id, copy_count, book_id),)

             # Save changes 
            conn.commit()

        return self.get_by_id(book_id)

    # Delete row from book table
    def delete(self, book_id: int) -> None:
        with Connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM Book WHERE book_id = %s", (book_id,), )

            # Save changes
            conn.commit()

# Member class
class MemberDAO:

    # Converts a DB dictionary into a Member data class
    def MapRow(self, row: dict) -> Member:
        return Member(
            member_id=row["member_id"],
            full_name=row["full_name"],
            email=row["email"],
            join_date=row["join_date"],
        )

    # Create member - add into database table
    def create(self, full_name: str, email: str, join_date: date) -> Member:
        with Connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("INSERT INTO Member (full_name, email, join_date) VALUES (%s, %s, %s)",
                    (full_name, email, join_date),
                )
                member_id = cursor.lastrowid
            conn.commit()
        return self.get_by_id(member_id)

    # Retrieve a single member by ID
    def get_by_id(self, member_id: int) -> Optional[Member]:
        with Connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT member_id, full_name, email, join_date FROM Member WHERE member_id = %s", (member_id,),)
                row = cursor.fetchone()
                return self.MapRow(row) if row else None

    # Retrieve all members
    def get_all(self) -> list[Member]:
        with Connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT member_id, full_name, email, join_date FROM Member ORDER BY member_id")
                return [self.MapRow(row) for row in cursor.fetchall()]

    # Update member table
    def update(
        self,
        member_id: int,
        full_name: str,
        email: str,
        join_date: date,
    ) -> Optional[Member]:
        with Connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Member SET full_name = %s, email = %s, join_date = %s WHERE member_id = %s",
                    (full_name, email, join_date, member_id),
                )
            conn.commit()
        return self.get_by_id(member_id)

    # Delete row from member table
    def delete(self, member_id: int) -> None:
        with Connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM Member WHERE member_id = %s",
                    (member_id,),
                )
            conn.commit()

# Loan class
class LoanDAO:

    # Converts a DB dictionary into a Loan data class
    def MapRow(self, row: dict) -> Loan:
        return Loan(
            loan_id=row["loan_id"],
            book_id=row["book_id"],
            member_id=row["member_id"],
            loan_date=row["loan_date"],
            due_date=row["due_date"],
            return_date=row["return_date"],
        )

    # Create loan - add into database table
    def create(
        self,
        book_id: int,
        member_id: int,
        loan_date: date,
        due_date: date,
    ) -> Loan:
        with Connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute
                (
                    "INSERT INTO Loan (book_id, member_id, loan_date, due_date) VALUES (%s, %s, %s, %s)",
                    (book_id, member_id, loan_date, due_date),
                )
                loan_id = cursor.lastrowid
            conn.commit()
        return self.get_by_id(loan_id)

    # Retrieve a single loan by ID
    def get_by_id(self, loan_id: int) -> Optional[Loan]:
        with Connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute
                (
                    "SELECT loan_id, book_id, member_id, loan_date, due_date, return_date FROM Loan WHERE loan_id = %s",
                    (loan_id,),
                )
                row = cursor.fetchone()
                return self.MapRow(row) if row else None

    # Retrieve all loans
    def get_all(self) -> list[Loan]:
        with Connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute
                (
                    "SELECT loan_id, book_id, member_id, loan_date, due_date, return_date FROM Loan ORDER BY loan_id"
                )

                return [self.MapRow(row) for row in cursor.fetchall()]

    # Retrieve all active loans (return_date is null)
    def get_active_loans(self) -> list[Loan]:
        with Connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute
                (
                    "SELECT loan_id, book_id, member_id, loan_date, due_date, return_date FROM Loan WHERE return_date IS NULL ORDER BY loan_id"
                )
                return [self.MapRow(row) for row in cursor.fetchall()]

    # Mark a loan as returned
    def return_book(self, loan_id: int, return_date: date) -> Optional[Loan]:
        with Connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute
                (
                    "UPDATE Loan SET return_date = %s WHERE loan_id = %s",
                    (return_date, loan_id),
                )
            conn.commit()
        return self.get_by_id(loan_id)

    # Delete row from loan table
    def delete(self, loan_id: int) -> None:
        with Connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM Loan WHERE loan_id = %s",
                    (loan_id,),
                )
            conn.commit()
