def create_views(db):
    with db.cursor() as cur:
        cur.execute(
            """
            CREATE OR REPLACE VIEW FreqLoanedGenre AS
            SELECT 
                G.name,
                COUNT(L.loan_id) AS BookCount
            FROM Book B
            INNER JOIN Genre G ON G.genre_id = B.genre_id
            INNER JOIN Loan L ON L.book_id = B.book_id
            GROUP BY G.name
            ORDER BY BookCount DESC;

            CREATE OR REPLACE VIEW MostActiveMembers AS
            SELECT
                M.full_name,
                COUNT(L.loan_id) AS LoanActivity
            FROM Member M
            LEFT JOIN Loan L ON L.member_id = M.member_id
            GROUP BY M.full_name
            ORDER BY LoanActivity DESC;

            CREATE OR REPLACE VIEW OverdueLoans AS
            SELECT loan_id
            FROM Loan
            WHERE return_date IS NULL AND due_date < CURRENT_DATE;
            """
        )
    db.commit()

def see_views(db):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT *
            FROM FreqLoanedGenre;
            """
        )
        results1 = cur.fetchall()
        cur.execute(
            """
            SELECT *
            FROM MostActiveMembers;
            """
        )
        results2 = cur.fetchall()
        cur.execute(
            """
            SELECT *
            FROM OverdueLoans;
            """
        )
        results3 = cur.fetchall()
    print(results1)
    print(results2)
    print(results3)