from src.db.connection import get_connection

class MemberDAO:

    # CREATE MEMBER
    def create(self, full_name, email_address, join_date):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO member (full_name, email_address, join_date)
                    VALUES (%s, %s, %s)
                    RETURNING member_id, full_name, email_address, join_date
                    """,
                    (full_name, email_address, join_date),
                )
                row = cur.fetchone()
                conn.commit()
                return row
    #GET MEMBER BY ID      
    def get_by_id(self, member_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT member_id, full_name, email_address, join_date
                    FROM member
                    WHERE member_id = %s
                    """,
                    (member_id,),
                )
                return cur.fetchone()
            
    #GET ALL MEMBERS   
    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT member_id, full_name, email_address, join_date
                    FROM member
                    """
                )
                return cur.fetchall()
            
    #UPDATE MEMBER         
    def update(self, member_id, full_name, email_address, join_date):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE member
                    SET full_name = %s, email_address = %s, join_date = %s
                    WHERE member_id = %s
                    RETURNING member_id, full_name, email_address, join_date
                    """,
                    (full_name, email_address, join_date, member_id),
                )
                row = cur.fetchone()
                conn.commit()
                return row
            
    #DELETE MEMBER        
    def delete(self, member_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM member
                    WHERE member_id = %s
                    RETURNING member_id
                    """,
                    (member_id,),
                )
                conn.commit()
                return cur.rowcount > 0