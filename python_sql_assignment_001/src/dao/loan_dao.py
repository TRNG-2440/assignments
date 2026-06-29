from src.db.connection import get_connection


class LoanDAO:

    def create(self, book_id, member_id, loan_date, due_date):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO loan (book_id, member_id, loan_date, due_date)
                    VALUES (%s, %s, %s, %s)
                    RETURNING loan_id, book_id, member_id, loan_date, due_date
                    """,
                    (book_id, member_id, loan_date, due_date),
                )
                row = cur.fetchone()
                conn.commit()
                return row
            
    def get_by_id(self, loan_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT loan_id, book_id, member_id, loan_date, due_date
                    FROM loan
                    WHERE loan_id = %s
                    """,
                    (loan_id,),
                )
                return cur.fetchone()
            
    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT loan_id, book_id, member_id, loan_date, due_date
                    FROM loan
                    """
                )
                return cur.fetchall()
            
    def get_active_loans(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT loan_id, book_id, member_id, loan_date, due_date
                    FROM loan
                    WHERE returned_date IS NULL
                    """
                )
                return cur.fetchall()
            
    def return_book(self, loan_id, returned_date):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE loan
                    SET returned_date = %s
                    WHERE loan_id = %s
                    RETURNING loan_id, book_id, member_id, loan_date, due_date, returned_date
                    """,
                    (returned_date, loan_id),
                )
                row = cur.fetchone()
                conn.commit()
                return row
            
    def delete(self, loan_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM loan
                    WHERE loan_id = %s
                    RETURNING loan_id
                    """,
                    (loan_id,),
                )

                conn.commit()
                return cur.rowcount > 0
        
    