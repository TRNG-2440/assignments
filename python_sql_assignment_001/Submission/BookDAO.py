from postgresCrudDAO import genericDao

class BookDAO:
    def __init__(self, dao:genericDao):
        self.dao = dao

    def create(self, title, author, publication_year, genre_id, copy_count):
        sql =   "INSERT INTO books (title, author_name, publication_year, genre_id, total_copies) " \
                "VALUES (%s, %s, %s, %s, %s) " \
                "RETURNING *"
        return self.dao.get_one(sql, (title, author, publication_year, genre_id, copy_count))

    def get_by_id(self, book_id):
        sql =   "SELECT * " \
                "FROM books " \
                "WHERE book_id = %s;"
        return self.dao.get_one(sql, (book_id,))

    def get_all(self):
        sql =   "SELECT * " \
                "FROM books;"
        return self.dao.get_all(sql)

    def update(self, book_id, title, author, publication_year, genre_id, copy_count):
        sql =   "UPDATE books " \
                "SET title = %s, " \
                    "author_name = %s, " \
                    "publication_year = %s, " \
                    "genre_id = %s, " \
                    "total_copies = %s " \
                "WHERE book_id = %s " \
                "RETURNING *;"
        return self.dao.get_one(sql, (title, author, publication_year, genre_id, copy_count, book_id))

    def delete(self, book_id):
        sql =   "DELETE FROM books " \
                "WHERE book_id = %s;"
        return self.dao.execute(sql, (book_id,))