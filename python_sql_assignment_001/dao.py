class GenreDAO():
    def __init__(self, db):
        self.db = db

    def create(self, name):
        with self.db.cursor() as cur:
            cur.execute(
                """
                INSERT INTO Genre (name)
                VALUES (%s)
                RETURNING genre_id;
                """, 
                (name,)
            )
            genre_id = cur.fetchone()[0]
        self.db.commit()
        return genre_id
    
    def get_by_id(self, genre_id):
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM Genre
                WHERE genre_id = %s;
                """,
                (genre_id,)
            )
            return cur.fetchone()
    
    def get_all(self):
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM Genre;
                """
            )
            return cur.fetchall()
    
    def update(self, genre_id, name):
        with self.db.cursor() as cur:
            cur.execute(
                """
                UPDATE Genre
                SET name = %s
                WHERE genre_id = %s;
                """,
                (name, genre_id)
            )
        self.db.commit()
    
    def delete(self, genre_id):
        with self.db.cursor() as cur:
            cur.execute(
                """
                DELETE FROM Genre
                WHERE genre_id = %s;
                """,
                (genre_id,)
            )
        self.db.commit()   

class BookDAO():
    def __init__(self, db):
        self.db = db
    
    def create(self, title, author, publication_year, genre_id, copy_count):
        with self.db.cursor() as cur:
            cur.execute(
                """
                INSERT INTO Book (title, author, publication_year, genre_id, copy_count)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING book_id;
                """, 
                (title, author, publication_year, genre_id, copy_count)
            )
            book_id = cur.fetchone()[0]
        self.db.commit()
        return book_id
    
    def get_by_id(self, book_id):
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM Book
                WHERE book_id = %s;
                """,
                (book_id,)
            )
            return cur.fetchone()
    
    def get_all(self):
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM Book;
                """
            )
            return cur.fetchall()
    
    def update(self, book_id, title, author, publication_year, genre_id, copy_count):
        with self.db.cursor() as cur:
            cur.execute(
                """
                UPDATE Book
                SET 
                    title = %s,
                    author = %s,
                    publication_year = %s,
                    genre_id = %s,
                    copy_count = %s
                WHERE book_id = %s;
                """,
                (title, author, publication_year, genre_id, copy_count, book_id)
            )
        self.db.commit()
    
    def delete(self, book_id):
        with self.db.cursor() as cur:
            cur.execute(
                """
                DELETE FROM Book
                WHERE book_id = %s;
                """,
                (book_id,)
            )
        self.db.commit()  

class MemberDAO():
    def __init__(self, db):
        self.db = db
    
    def create(self, full_name, email, join_date):
        with self.db.cursor() as cur:
            cur.execute(
                """
                INSERT INTO Member (full_name, email, join_date)
                VALUES (%s, %s, %s)
                RETURNING member_id;
                """, 
                (full_name, email, join_date)
            )
            member_id = cur.fetchone()[0]
        self.db.commit()
        return member_id
    
    def get_by_id(self, member_id):
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM Member
                WHERE member_id = %s;
                """,
                (member_id,)
            )
            return cur.fetchone()
    
    def get_all(self):
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM Member;
                """
            )
            return cur.fetchall()
    
    def update(self, member_id, full_name, email, join_date):
        with self.db.cursor() as cur:
            cur.execute(
                """
                UPDATE Member
                SET 
                    full_name = %s,
                    email = %s,
                    join_date = %s
                WHERE member_id = %s;
                """,
                (full_name, email, join_date, member_id)
            )
        self.db.commit()
    
    def delete(self, member_id):
        with self.db.cursor() as cur:
            cur.execute(
                """
                DELETE FROM Member
                WHERE member_id = %s;
                """,
                (member_id,)
            )
        self.db.commit()  
        
class LoanDAO():
    def __init__(self, db):
        self.db = db
    
    def create(self, book_id, member_id, loan_date, due_date):
        with self.db.cursor() as cur:
            cur.execute(
                """
                INSERT INTO Loan (book_id, member_id, loan_date, due_date)
                VALUES (%s, %s, %s, %s)
                RETURNING loan_id;
                """, 
                (book_id, member_id, loan_date, due_date)
            )
            loan_id = cur.fetchone()[0]
        self.db.commit()
        return loan_id
    
    def get_by_id(self, loan_id):
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM Loan
                WHERE loan_id = %s;
                """,
                (loan_id,)
            )
            return cur.fetchone()
    
    def get_all(self):
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM Loan;
                """
            )
            return cur.fetchall()
    
    def update(self, loan_id, book_id, member_id, loan_date, due_date):
        with self.db.cursor() as cur:
            cur.execute(
                """
                UPDATE Loan
                SET 
                    book_id = %s,
                    member_id = %s,
                    loan_date = %s,
                    due_date = %s
                WHERE loan_id = %s;
                """,
                (book_id, member_id, loan_date, due_date, loan_id)
            )
        self.db.commit()
    
    def delete(self, loan_id):
        with self.db.cursor() as cur:
            cur.execute(
                """
                DELETE FROM Loan
                WHERE loan_id = %s;
                """,
                (loan_id,)
            )
        self.db.commit()  
        
        