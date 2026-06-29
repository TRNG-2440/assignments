import dao as D
import models as M
from fastapi import FastAPI
from datetime import date
from db_util import connection_details
import db_util

genre_dao = D.GenreDAO()
book_dao = D.BookDAO()
member_dao = D.MemberDAO()
loan_dao = D.LoanDAO()

db_util.del_schema()
db_util.init_db()
input("enter to continue")

gen1 = D.GenreRecord(genre_id=None, genre_name="Fiction")
gen2 = D.GenreRecord(genre_id=None, genre_name="Non-Fiction")

book1 = D.BookRecord(None, 1, "Artemis", "Andy Weir", 2017, 5)
book2 = D.BookRecord(None, 2, "All Systems Red", "Martha Wells", 2018, 5)

member1 = D.MemberRecord(None, "Lionel Polanski", "lp@email.com", date.today())
member2 = D.MemberRecord(None, "Doug Judy", "dj@email.com", date.today())

loan1 = D.LoanRecord(None, 1, 1, date.today(), date.fromisoformat("2026-07-10"), None)
loan2 = D.LoanRecord(None, 2, 2, date.today(), date.fromisoformat("2026-07-10"), None)

genre_dao.create(gen1)
genre_dao.create(gen2)

book_dao.create(book1)
book_dao.create(book2)

member_dao.create(member1)
member_dao.create(member2)

loan_dao.create(loan1)
loan_dao.create(loan2)

read_member = member_dao.get_by_id(1)

print(read_member.title, read_member.inventory)


update_member = D.MemberRecord(1, read_member.member_name, "new@email.com", read_member.date_joined)
updated = member_dao.update(update_member)
read_member = member_dao.get_by_id(1)

print(updated.title, updated.inventory)
print(read_member.title, read_member.inventory)

deleted = member_dao.delete(1)

check_deleted = member_dao.get_by_id(1)

if check_deleted is not None:
    print(check_deleted.member_name)
if deleted:
    print("member deleted")