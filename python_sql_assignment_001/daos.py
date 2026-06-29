
class GenreDao:
    def __init__(self, conn):
        self.conn = conn

    def create(self, name):
        cursor = self.conn.execute(
            '''
            INSERT INTO genre(genre_name)
            VALUES (?)
            ''',
            (name,)
        )
        self.conn.commit()

        return self.get_by_id(cursor.lastrowid)
    
    def get_by_id(self, genre_id):
        cursor = self.conn.execute(
            "SELECT * FROM genre WHERE genre_id = ?",
            (genre_id,)
        )
        return cursor.fetchone()
    
    def get_all(self):
        cursor = self.conn.execute(
            "SELECT * FROM genre"
        )
        return cursor.fetchall()
    
    def update(self, genre_id, name):
        self.conn.execute(
            '''
            UPDATE genre
            SET name = ?
            WHERE genre_id = ?
            ''',
            (name, genre_id)
        )
        self.conn.commit()

        return self.get_by_id(genre_id)

    def delete(self, genre_id):
        self.conn.execute(
            '''
            DELETE FROM genre
            where genre_id = ?
            ''',
            (genre_id,)
        )
        self.conn.commit()

class BookDAO:
    def __init__(self, conn):
        self.conn = conn

    def create(self, title, author, publication_year, genre_id, copy_count):
        cursor = self.conn.execute(
            '''
            INSERT INTO book(book_title, book_author, book_year, book_genre, book_copies)
            VALUES (?,?,?,?,?)
            ''',
            (title, author, publication_year, genre_id, copy_count)
        )
        self.conn.commit()

        return self.get_by_id(cursor.lastrowid)
    
    def get_by_id(self, book_id):
        cursor = self.conn.execute(
            '''
            SELECT * FROM book
            WHERE book_id = ?
            ''',
            (book_id,)
        )
        return cursor.fetchone()
    
    def get_all(self):
        cursor = self.conn.execute(
            "SELECT * FROM book"
        )
        return cursor.fetchall()

    def update(self, book_id, title, author, publication_year, genre_id, copy_count):
        self.conn.execute(
            '''
            UPDATE book
            SET book_title = ?,
            book_author = ?,
            book_year = ?,
            book_genre = ?,
            book_copies = ?
            WHERE book_id = ?
            ''',
            (title, author, publication_year, genre_id, copy_count, book_id)
        )
        self.conn.commit()

        return self.get_by_id(book_id)
    
    def delete(self, book_id):
        self.conn.execute(
            '''
            DELETE FROM book
            where book_id = ?
            ''',
            (book_id,)
        )
        self.conn.commit()

class MemberDAO:
    def __init__(self, conn):
        self.conn = conn

    def create(self, full_name, email, join_date):
        cursor = self.conn.execute(
            '''
            INSERT INTO member(member_name, member_email, join_date)
            VALUES (?,?,?)
            ''',
            (full_name, email, join_date)
        )
        self.conn.commit()

        return self.get_by_id(cursor.lastrowid)
    
    def get_by_id(self, member_id):
        cursor = self.conn.execute(
            '''
            SELECT * FROM member
            WHERE member_id = ?
            ''',
            (member_id,)
        )
        return cursor.fetchone()
    
    def get_all(self):
        cursor = self.conn.execute(
            "SELECT * FROM member"
        )
        return cursor.fetchall()

    def update(self, member_id, full_name, email, join_date):
        self.conn.execute(
            '''
            UPDATE member
            SET member_name = ?,
            member_email = ?,
            join_date = ?
            WHERE member_id = ?
            ''',
            (full_name, email, join_date, member_id)
        )
        self.conn.commit()

        return self.get_by_id(member_id)
    
    def delete(self, member_id):
        self.conn.execute(
            '''
            DELETE FROM member
            where member_id = ?
            ''',
            (member_id,)
        )
        self.conn.commit()

class LoanDAO:
    def __init__(self, conn):
        self.conn = conn

    def create(self, book_id, member_id, loan_date, due_date):
        cursor = self.conn.execute(
            '''
            INSERT INTO loan(loan_book, loan_member, loan_date, loan_due)
            VALUES (?,?,?,?)
            ''',
            (book_id, member_id, loan_date, due_date)
        )
        self.conn.commit()

        return self.get_by_id(cursor.lastrowid)
    
    def get_by_id(self, loan_id):
        cursor = self.conn.execute(
            '''
            SELECT * FROM loan
            WHERE loan_id = ?
            ''',
            (loan_id,)
        )
        return cursor.fetchone()
    
    def get_active_loans(self):
        cursor = self.conn.execute(
            "SELECT * FROM loan"
        )
        return cursor.fetchall()

    def return_book(self, loan_id, return_date):
        self.conn.execute(
            '''
            UPDATE loan
            SET loan_return_date = ?
            WHERE loan_id = ?
            ''',
            (return_date, loan_id)
        )
        self.conn.commit()

        return self.get_by_id(loan_id)
    
    def delete(self, loan_id):
        self.conn.execute(
            '''
            DELETE FROM loan
            where loan_id = ?
            ''',
            (loan_id,)
        )
        self.conn.commit()
