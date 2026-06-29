from src.db.connection import get_connection

class GenreDAO:
    
    def create(self, genre_name):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO genre (genre_name)
                    VALUES (%s)
                    RETURNING genre_id, genre_name
                    """,
                    (genre_name,)
                )
                row = cur.fetchone()
                conn.commit()

                return row
            
    def get_by_id(self, genre_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT genre_id, genre_name
                    FROM genre
                    WHERE genre_id = %s
                    """,
                    (genre_id,)
                )
                return cur.fetchone()
            
            
    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT genre_id, genre_name
                    FROM genre
                    """
                )
                return cur.fetchall()
            

    def update(self, genre_id, genre_name):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE genre
                    SET genre_name = %s
                    WHERE genre_id = %s
                    RETURNING genre_id, genre_name
                    """,
                    (genre_name, genre_id)
                )
                row = cur.fetchone()
                conn.commit()
                return row
            
    def delete(self, genre_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM genre
                    WHERE genre_id = %s
                    RETURNING genre_id
                    """,
                    (genre_id,)
                )
                conn.commit()
                return cur.rowcount > 0