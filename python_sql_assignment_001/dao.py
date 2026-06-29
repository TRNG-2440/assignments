"""Data access objects for the library tables.

One class per table, each implementing the standard CRUD operations. Every
value is passed as a query parameter, never formatted into the SQL string.
Create and update methods use RETURNING * so the stored row is handed back.
"""

from psycopg2.extras import RealDictCursor


class GenreDAO:
    def __init__(self, conn):
        self.conn = conn

    def create(self, name):
        sql = "INSERT INTO genre (name) VALUES (%s) RETURNING *;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (name,))
            row = cur.fetchone()
        self.conn.commit()
        return row

    def get_by_id(self, genre_id):
        sql = "SELECT * FROM genre WHERE genre_id = %s;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (genre_id,))
            row = cur.fetchone()
        return row

    def get_all(self):
        sql = "SELECT * FROM genre ORDER BY genre_id;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
        return rows

    def update(self, genre_id, name):
        sql = "UPDATE genre SET name = %s WHERE genre_id = %s RETURNING *;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (name, genre_id))
            row = cur.fetchone()
        self.conn.commit()
        return row

    def delete(self, genre_id):
        sql = "DELETE FROM genre WHERE genre_id = %s RETURNING *;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (genre_id,))
            row = cur.fetchone()
        self.conn.commit()
        return row


class BookDAO:
    def __init__(self, conn):
        self.conn = conn

    def create(self, title, author, publication_year, genre_id, copy_count):
        sql = (
            "INSERT INTO book (title, author, publication_year, genre_id, copy_count) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING *;"
        )
        params = (title, author, publication_year, genre_id, copy_count)
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            row = cur.fetchone()
        self.conn.commit()
        return row

    def get_by_id(self, book_id):
        sql = "SELECT * FROM book WHERE book_id = %s;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (book_id,))
            row = cur.fetchone()
        return row

    def get_all(self):
        sql = "SELECT * FROM book ORDER BY book_id;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
        return rows

    def update(self, book_id, title, author, publication_year, genre_id, copy_count):
        sql = (
            "UPDATE book "
            "SET title = %s, author = %s, publication_year = %s, "
            "    genre_id = %s, copy_count = %s "
            "WHERE book_id = %s RETURNING *;"
        )
        params = (title, author, publication_year, genre_id, copy_count, book_id)
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            row = cur.fetchone()
        self.conn.commit()
        return row

    def delete(self, book_id):
        sql = "DELETE FROM book WHERE book_id = %s RETURNING *;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (book_id,))
            row = cur.fetchone()
        self.conn.commit()
        return row


class MemberDAO:
    def __init__(self, conn):
        self.conn = conn

    def create(self, full_name, email, join_date):
        sql = (
            "INSERT INTO member (full_name, email, join_date) "
            "VALUES (%s, %s, %s) RETURNING *;"
        )
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (full_name, email, join_date))
            row = cur.fetchone()
        self.conn.commit()
        return row

    def get_by_id(self, member_id):
        sql = "SELECT * FROM member WHERE member_id = %s;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (member_id,))
            row = cur.fetchone()
        return row

    def get_all(self):
        sql = "SELECT * FROM member ORDER BY member_id;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
        return rows

    def update(self, member_id, full_name, email, join_date):
        sql = (
            "UPDATE member "
            "SET full_name = %s, email = %s, join_date = %s "
            "WHERE member_id = %s RETURNING *;"
        )
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (full_name, email, join_date, member_id))
            row = cur.fetchone()
        self.conn.commit()
        return row

    def delete(self, member_id):
        sql = "DELETE FROM member WHERE member_id = %s RETURNING *;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (member_id,))
            row = cur.fetchone()
        self.conn.commit()
        return row


class LoanDAO:
    def __init__(self, conn):
        self.conn = conn

    def create(self, book_id, member_id, loan_date, due_date):
        sql = (
            "INSERT INTO loan (book_id, member_id, loan_date, due_date) "
            "VALUES (%s, %s, %s, %s) RETURNING *;"
        )
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (book_id, member_id, loan_date, due_date))
            row = cur.fetchone()
        self.conn.commit()
        return row

    def get_by_id(self, loan_id):
        sql = "SELECT * FROM loan WHERE loan_id = %s;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (loan_id,))
            row = cur.fetchone()
        return row

    def get_all(self):
        sql = "SELECT * FROM loan ORDER BY loan_id;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
        return rows

    def get_active_loans(self):
        sql = "SELECT * FROM loan WHERE return_date IS NULL ORDER BY loan_id;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
        return rows

    def return_book(self, loan_id, return_date):
        sql = "UPDATE loan SET return_date = %s WHERE loan_id = %s RETURNING *;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (return_date, loan_id))
            row = cur.fetchone()
        self.conn.commit()
        return row

    def delete(self, loan_id):
        sql = "DELETE FROM loan WHERE loan_id = %s RETURNING *;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (loan_id,))
            row = cur.fetchone()
        self.conn.commit()
        return row
