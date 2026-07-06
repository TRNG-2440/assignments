from postgresCrudDAO import genericDao

class GenreDAO:
    def __init__(self, dao:genericDao):
        self.dao = dao

    def create(self, genre_name):
        sql =   "INSERT INTO genres (genre_name) " \
                "VALUES (%s) RETURNING *"
        return self.dao.get_one(sql, (genre_name,))

    def get_by_id(self, genre_id):
        sql =   "SELECT * " \
                "FROM genres " \
                "WHERE genre_id = %s"
        return self.dao.get_one(sql, (genre_id,))

    def get_all(self):
        sql =   "SELECT * " \
                "FROM genres"
        return self.dao.get_all(sql)

    def update(self, genre_id, name):
        sql =   "UPDATE genres " \
                "SET genre_name = %s " \
                "WHERE genre_id = %s RETURNING *"
        return self.dao.get_one(sql, (name, genre_id))

    def delete(self, genre_id):
        sql =   "DELETE FROM genres " \
                "WHERE genre_id = %s"
        return self.dao.execute(sql, (genre_id,))