class GenreDAO:
    def __init__(self, conn):
        self.conn = conn

    def create(self, name):
        cursor = self.conn.execute("INSERT INTO Genre (name) VALUES (?)", (name,))
        self.conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def get_by_id(self, genre_id):
        cursor = self.conn.execute("SELECT * FROM Genre WHERE genre_id = ?", (genre_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return dict(row)

    def get_all(self):
        cursor = self.conn.execute("SELECT * FROM Genre")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(dict(row))
        return result

    def update(self, genre_id, name):
        self.conn.execute("UPDATE Genre SET name = ? WHERE genre_id = ?", (name, genre_id))
        self.conn.commit()
        return self.get_by_id(genre_id)

    def delete(self, genre_id):
        self.conn.execute("DELETE FROM Genre WHERE genre_id = ?", (genre_id,))
        self.conn.commit()


class BookDAO:
    def __init__(self, conn):
        self.conn = conn

    def create(self, title, author, publication_year, genre_id, copy_count):
        cursor = self.conn.execute(
            "INSERT INTO Book (title, author, publication_year, genre_id, copy_count) VALUES (?, ?, ?, ?, ?)",
            (title, author, publication_year, genre_id, copy_count)
        )
        self.conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def get_by_id(self, book_id):
        cursor = self.conn.execute("SELECT * FROM Book WHERE book_id = ?", (book_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return dict(row)

    def get_all(self):
        cursor = self.conn.execute("SELECT * FROM Book")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(dict(row))
        return result

    def update(self, book_id, title, author, publication_year, genre_id, copy_count):
        self.conn.execute(
            "UPDATE Book SET title = ?, author = ?, publication_year = ?, genre_id = ?, copy_count = ? WHERE book_id = ?",
            (title, author, publication_year, genre_id, copy_count, book_id)
        )
        self.conn.commit()
        return self.get_by_id(book_id)

    def delete(self, book_id):
        self.conn.execute("DELETE FROM Book WHERE book_id = ?", (book_id,))
        self.conn.commit()


class MemberDAO:
    def __init__(self, conn):
        self.conn = conn

    def create(self, full_name, email, join_date):
        cursor = self.conn.execute(
            "INSERT INTO Member (full_name, email, join_date) VALUES (?, ?, ?)",
            (full_name, email, join_date)
        )
        self.conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def get_by_id(self, member_id):
        cursor = self.conn.execute("SELECT * FROM Member WHERE member_id = ?", (member_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return dict(row)

    def get_all(self):
        cursor = self.conn.execute("SELECT * FROM Member")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(dict(row))
        return result

    def update(self, member_id, full_name, email, join_date):
        self.conn.execute(
            "UPDATE Member SET full_name = ?, email = ?, join_date = ? WHERE member_id = ?",
            (full_name, email, join_date, member_id)
        )
        self.conn.commit()
        return self.get_by_id(member_id)

    def delete(self, member_id):
        self.conn.execute("DELETE FROM Member WHERE member_id = ?", (member_id,))
        self.conn.commit()


class LoanDAO:
    def __init__(self, conn):
        self.conn = conn

    def create(self, book_id, member_id, loan_date, due_date):
        cursor = self.conn.execute(
            "INSERT INTO Loan (book_id, member_id, loan_date, due_date, return_date) VALUES (?, ?, ?, ?, NULL)",
            (book_id, member_id, loan_date, due_date)
        )
        self.conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def get_by_id(self, loan_id):
        cursor = self.conn.execute("SELECT * FROM Loan WHERE loan_id = ?", (loan_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return dict(row)

    def get_all(self):
        cursor = self.conn.execute("SELECT * FROM Loan")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(dict(row))
        return result

    def get_active_loans(self):
        cursor = self.conn.execute("SELECT * FROM Loan WHERE return_date IS NULL")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(dict(row))
        return result

    def return_book(self, loan_id, return_date):
        self.conn.execute("UPDATE Loan SET return_date = ? WHERE loan_id = ?", (return_date, loan_id))
        self.conn.commit()
        return self.get_by_id(loan_id)

    def delete(self, loan_id):
        self.conn.execute("DELETE FROM Loan WHERE loan_id = ?", (loan_id,))
        self.conn.commit()