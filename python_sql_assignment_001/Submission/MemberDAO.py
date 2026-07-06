from postgresCrudDAO import genericDao


class MemberDAO:
    def __init__(self, dao: genericDao):
        self.dao = dao

    def create(self, full_name, email, join_date):
        sql = (
            "INSERT INTO members (full_name, email, join_date) "
            "VALUES (%s, %s, %s) "
            "RETURNING *;"
        )
        return self.dao.get_one(sql, (full_name, email, join_date))

    def get_by_id(self, member_id):
        sql = (
            "SELECT * "
            "FROM members "
            "WHERE member_id = %s;"
        )
        return self.dao.get_one(sql, (member_id,))

    def get_all(self):
        sql = (
            "SELECT * "
            "FROM members;"
        )
        return self.dao.get_all(sql)

    def update(self, member_id, full_name, email, join_date):
        sql = (
            "UPDATE members "
            "SET full_name = %s, "
            "email = %s, "
            "join_date = %s "
            "WHERE member_id = %s "
            "RETURNING *;"
        )
        return self.dao.get_one(sql, (full_name, email, join_date, member_id))

    def delete(self, member_id):
        sql = (
            "DELETE FROM members "
            "WHERE member_id = %s;"
        )
        return self.dao.execute(sql, (member_id,))