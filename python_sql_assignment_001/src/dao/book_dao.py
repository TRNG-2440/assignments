from src.db.connection import get_connection

class BookDAO:

    #CREATE
    def create(self, title, author_name, publication_year, genre_id, copies_count):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO book (title, author_name, publication_year, genre_id, copies_count)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING book_id, title, author_name, publication_year, genre_id, copies_count
                    """,
                    (title, author_name, publication_year, genre_id, copies_count)
                )
                row = cur.fetchone()
                conn.commit()
                return row
    
    #GET BY ID
    def get_by_id(self, book_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT book_id, title, author_name, publication_year, genre_id, copies_count
                    FROM book
                    WHERE book_id = %s
                    """,
                    (book_id,)
                )
                return cur.fetchone()

    #READ ALL        
    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT book_id, title, author_name, publication_year, genre_id, copies_count
                    FROM book
                    """
                )
                return cur.fetchall()
    
    #UPDATE      
    def update(self, book_id, title, author_name, publication_year, genre_id, copies_count):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE book
                    SET title = %s, author_name = %s, publication_year = %s, genre_id = %s, copies_count = %s
                    WHERE book_id = %s
                    RETURNING book_id, title, author_name, publication_year, genre_id, copies_count
                    """,
                    (title, author_name, publication_year, genre_id, copies_count, book_id)
                )
                row = cur.fetchone()
                conn.commit()
                return row
            

    #DELETE
    def delete(self, book_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM book
                    WHERE book_id = %s
                    RETURNING book_id
                    """,
                    (book_id,)
                )
                conn.commit()
                return cur.rowcount > 0