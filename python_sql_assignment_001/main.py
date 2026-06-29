from database import get_connection, initialize_db
from dao import GenreDAO, BookDAO, MemberDAO, LoanDAO

conn = get_connection()
initialize_db(conn)

genre_dao = GenreDAO(conn)
book_dao = BookDAO(conn)
member_dao = MemberDAO(conn)
loan_dao = LoanDAO(conn)

print("--- INSERTING GENRES ---")
fiction = genre_dao.create("Fiction")
mystery = genre_dao.create("Mystery")
print(fiction)
print(mystery)

print("--- INSERTING BOOKS ---")
book1 = book_dao.create("The Great Gatsby", "F. Scott Fitzgerald", 1925, fiction["genre_id"], 4)
book2 = book_dao.create("Sherlock Holmes", "Arthur Conan Doyle", 1892, mystery["genre_id"], 2)
print(book1)
print(book2)

print("--- INSERTING MEMBERS ---")
member1 = member_dao.create("John Doe", "john@email.com", "2024-01-01")
member2 = member_dao.create("Jane Doe", "jane@email.com", "2024-02-01")
print(member1)
print(member2)

print("--- INSERTING LOANS ---")
loan1 = loan_dao.create(book1["book_id"], member1["member_id"], "2024-03-01", "2024-03-15")
loan2 = loan_dao.create(book2["book_id"], member2["member_id"], "2024-03-05", "2024-03-20")
print(loan1)
print(loan2)

print("--- READING DATA ---")
print(genre_dao.get_all())
print(book_dao.get_by_id(book1["book_id"]))
print(loan_dao.get_active_loans())

print("--- UPDATING DATA ---")
updated_member = member_dao.update(member1["member_id"], "John Smith", "johnsmith@email.com", "2024-01-01")
print(updated_member)

print("--- RETURNING A BOOK ---")
returned = loan_dao.return_book(loan1["loan_id"], "2024-03-10")
print(returned)

print("--- DELETING DATA ---")
loan_dao.delete(loan2["loan_id"])
book_dao.delete(book2["book_id"])
print("Remaining books:")
print(book_dao.get_all())

conn.close()