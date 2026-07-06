from postgresCrudDAO import genericDao

class LoanDAO:
    def __init__(self, dao: genericDao):
        self.dao = dao

    def create(self, book_id, member_id, loan_date, due_date):
        sql = (
            "INSERT INTO loans (book_id, member_id, loan_date, due_date) "
            "VALUES (%s, %s, %s, %s) "
            "RETURNING *;"
        )
        return self.dao.get_one(sql, (book_id, member_id, loan_date, due_date))

    def get_by_id(self, loan_id):
        sql = (
            "SELECT * "
            "FROM loans "
            "WHERE loan_id = %s;"
        )
        return self.dao.get_one(sql, (loan_id,))

    def get_all(self):
        sql = (
            "SELECT * "
            "FROM loans;"
        )
        return self.dao.get_all(sql)

    def get_active_loans(self):
        sql = (
            "SELECT * "
            "FROM loans "
            "WHERE return_date IS NULL;"
        )
        return self.dao.get_all(sql)

    def return_book(self, loan_id, return_date):
        sql = (
            "UPDATE loans "
            "SET return_date = %s "
            "WHERE loan_id = %s "
            "RETURNING *;"
        )
        return self.dao.get_one(sql, (return_date, loan_id))

    def delete(self, loan_id):
        sql = (
            "DELETE FROM loans "
            "WHERE loan_id = %s;"
        )
        return self.dao.execute(sql, (loan_id,))