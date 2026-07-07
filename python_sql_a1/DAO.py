from db import get_connection

class GenreDAO:
    @staticmethod
    def create(name):
        with get_connection() as conn:
            cursor = conn.execute("INSERT INTO Genre (name) VALUES (?)", (name,))
            return GenreDAO.get_by_id(cursor.lastrowid)
        
    @staticmethod
    def get_all():
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM Genre").fetchall()
        
        result_list = []
        for r in rows:
            result_list.append(dict(r))
            
        return result_list

    @staticmethod
    def get_by_id(genre_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM Genre WHERE genre_id = ?", (genre_id,)).fetchone()
            return dict(row) if row else None


    @staticmethod
    def update(genre_id, name):
        with get_connection() as conn:
            conn.execute("UPDATE Genre SET name = ? WHERE genre_id = ?", (name, genre_id))
            return GenreDAO.get_by_id(genre_id)

    @staticmethod
    def delete(genre_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM Genre WHERE genre_id = ?", (genre_id,))


class BookDAO:
    @staticmethod
    def create(title, author, publication_year, genre_id, copy_count):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO Book (title, author, publication_year, genre_id, copy_count) VALUES (?, ?, ?, ?, ?)",
                (title, author, publication_year, genre_id, copy_count)
            )
            return BookDAO.get_by_id(cursor.lastrowid)

    @staticmethod
    def get_by_id(book_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM Book WHERE book_id = ?", (book_id,)).fetchone()
        
        if row:
            return dict(row)
        else:
            return None

    @staticmethod
    def get_all():
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM Book").fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def update(book_id, title, author, publication_year, genre_id, copy_count):
        with get_connection() as conn:
            conn.execute(
                "UPDATE Book SET title = ?, author = ?, publication_year = ?, genre_id = ?, copy_count = ? WHERE book_id = ?",
                (title, author, publication_year, genre_id, copy_count, book_id)
            )
            return BookDAO.get_by_id(book_id)

    @staticmethod
    def delete(book_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM Book WHERE book_id = ?", (book_id,))


class MemberDAO:
    @staticmethod
    def create(full_name, email, join_date):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO Member (full_name, email, join_date) VALUES (?, ?, ?)",
                (full_name, email, join_date)
            )
            return MemberDAO.get_by_id(cursor.lastrowid)

    @staticmethod
    def get_by_id(member_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM Member WHERE member_id = ?", (member_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_all():
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM Member").fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def update(member_id, full_name, email, join_date):
        with get_connection() as conn:
            conn.execute(
                "UPDATE Member SET full_name = ?, email = ?, join_date = ? WHERE member_id = ?",
                (full_name, email, join_date, member_id)
            )
            return MemberDAO.get_by_id(member_id)

    @staticmethod
    def delete(member_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM Member WHERE member_id = ?", (member_id,))


class LoanDAO:
    @staticmethod
    def create(book_id, member_id, loan_date, due_date):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO Loan (book_id, member_id, loan_date, due_date, return_date) VALUES (?, ?, ?, ?, NULL)",
                (book_id, member_id, loan_date, due_date)
            )
            return LoanDAO.get_by_id(cursor.lastrowid)

    @staticmethod
    def get_by_id(loan_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM Loan WHERE loan_id = ?", (loan_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_all():
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM Loan").fetchall()
        
        result_list = []
        for r in rows:
            result_list.append(dict(r))
            
        return result_list

@staticmethod
def get_active_loans():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM Loan WHERE return_date IS NULL").fetchall()
        
        active_loans_list = []
        for r in rows:
            active_loans_list.append(dict(r))
            
        return active_loans_list
    
    @staticmethod
    def return_book(loan_id, return_date):
        with get_connection() as conn:
            conn.execute("UPDATE Loan SET return_date = ? WHERE loan_id = ?", (return_date, loan_id))
            return LoanDAO.get_by_id(loan_id)

    @staticmethod
    def delete(loan_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM Loan WHERE loan_id = ?", (loan_id,))