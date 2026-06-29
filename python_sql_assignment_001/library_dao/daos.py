from db import get_connection


class GenreDAO():
    def create(self, name):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO genre (name) VALUES (%s) RETURNING *;",
                    (name,)
                )
                return cur.fetchone()
    
    def get_by_id(self, genre_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM genre_id WHERE genre_id = %s;",
                    (genre_id, )
                )
                return cur.fetchone()
    
    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM genre_id ORDER BY genre_id;")
                return cur.fetchall()
            
    def update(self, genre_id, name):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE genre
                    SET name = %s
                    WHERE genre_id = %s
                    RETURNING *;
                    """,
                    (name, genre_id)
                )
                return cur.fetchone()
    def delete(self, genre_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM genre WHERE genre_id = %s RETURNING *;",
                    (genre_id,)
                )
                return cur.fetchone()
            
class BookDAO():
    def create(self, title, author, publication_year, genre_id, copy_count):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO book
                    (title, author, publication_year, genre_id, copy_count)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING *;
                    """,
                    (title, author, publication_year, genre_id, copy_count)
                )
                return cur.fetchone()
        
    def get_by_id(self, book_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM book WHERE book_id = %s;",
                    (book_id, )
                )
                return cur.fetchone()
    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM book ORDER BY book_id;"

                )
                return cur.fetchall()
    def update(self, book_id, title, author, publication_year, genre_id, copy_count):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE book 
                    SET title = %s,
                        author = %s,
                        publication_year = %s,
                        genre_id = %s,
                        copy_count = %s
                    WHERE book_id = %s
                    RETURNING *;
                    """,
                    (title, author, publication_year, genre_id, copy_count, book_id)
                )
                return cur.fetchone()
    
    def delete(self, book_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM book WHERE book_id = %s RETURNING *;",
                    (book_id,)
                )
                return cur.fetchone()
    

class MemberDAO():

    def create(self, full_name, email, join_date):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO member(full_name, email, join_date)
                    VALUES (%s, %s, %s)
                    RETURNING *;
                    """,
                    (full_name, email, join_date)
                )
                return cur.fetchone()
    
    def get_by_id(self, member_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM member WHERE member_id = %s;",
                    (member_id,)
                )
                return cur.fetchone()
    
    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM member ORDER BY member_id;"
                )
                return cur.fetchall()
    
    def update(self, member_id, full_name, email, join_date):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE member
                    SET full_name = %s,
                        email = %s,
                        join_date = %s
                    WHERE member_id = %s
                    RETURNING *;
                    """,
                    (full_name, email, join_date, member_id)
                )
                return cur.fetchone()
    
    def delete(self, member_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM member WHERE member_id = %s RETURNING *;",
                    (member_id, )
                )
                return cur.fetchone()
            
class LoanDAO():

    def create(self, book_id, member_id, loan_date, due_date):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO loan (book_id, member_id, loan_date, due_date)
                    VALUES (%s, %s, %s, %s)
                    RETURNING *;
                    """,
                    (book_id, member_id, loan_date, due_date)
                )
                return cur.fetchone()
    def get_by_id(self, loan_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM loan WHERE loan_id = %s;",
                    (loan_id, )
                )
                return cur.fetchone()
    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM loan ORDER BY loan_id;"
                )
                return cur.fetchall()
    
    def get_active_loans(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT * 
                    FROM loan
                    WHERE return_date IS NULL
                    ORDER BY loan_id;
                    """
                )
                return cur.fetchall()
    def return_books(self, loan_id, return_date):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE loan
                    SET return_date = %s
                    WHERE loan_id = %s
                    RETURNING *;
                    """,
                    (return_date, loan_id)
                )
                return cur.fetchone()
    def delete(self, loan_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM loan WHERE loan_id = %s RETURNING *;",
                    (loan_id, )
                )
                return cur.fetchone()



