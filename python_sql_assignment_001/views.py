"""Library statistics views: creation and queries (stretch goal 2)."""

from psycopg2.extras import RealDictCursor

VIEWS_SQL = """
1. Most frequently loaned genre.
-- LEFT JOINs keep genres that have never been loaned (count 0).
CREATE OR REPLACE VIEW most_loaned_genre AS
SELECT g.genre_id,
       g.name             AS genre_name,
       COUNT(l.loan_id)   AS loan_count
FROM genre g
LEFT JOIN book b ON b.genre_id = g.genre_id
LEFT JOIN loan l ON l.book_id = b.book_id
GROUP BY g.genre_id, g.name
ORDER BY loan_count DESC;

2. Most active members.
-- LEFT JOIN keeps members with no loans (count 0).
CREATE OR REPLACE VIEW most_active_members AS
SELECT m.member_id,
       m.full_name,
       COUNT(l.loan_id) AS loan_count
FROM member m
LEFT JOIN loan l ON l.member_id = m.member_id
GROUP BY m.member_id, m.full_name
ORDER BY loan_count DESC;

3. Overdue loans: not returned and past their due date.
CREATE OR REPLACE VIEW overdue_loans AS
SELECT l.loan_id,
       m.full_name,
       b.title,
       l.due_date,
       (CURRENT_DATE - l.due_date) AS days_overdue
FROM loan l
JOIN member m ON m.member_id = l.member_id
JOIN book b   ON b.book_id = l.book_id
WHERE l.return_date IS NULL
  AND l.due_date < CURRENT_DATE
ORDER BY days_overdue DESC;
"""


def create_views(conn):
    """Create the three statistics views."""
    with conn.cursor() as cur:
        cur.execute(VIEWS_SQL)
    conn.commit()


class StatsDAO:
    def __init__(self, conn):
        self.conn = conn

    def most_loaned_genres(self):
        sql = "SELECT * FROM most_loaned_genre;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
        return rows

    def most_active_members(self):
        sql = "SELECT * FROM most_active_members;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
        return rows

    def overdue_loans(self):
        sql = "SELECT * FROM overdue_loans;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
        return rows
