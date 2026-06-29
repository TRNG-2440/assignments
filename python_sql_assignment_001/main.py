"""Demonstration of the library DAO layer.

Run with:  python main.py

Initializes the schema, creates the statistics views, inserts sample records
into every table, then walks through read / update / delete and the views.
"""

import datetime

from database import get_connection, initialize_db
from dao import GenreDAO, BookDAO, MemberDAO, LoanDAO
from views import create_views, StatsDAO


def show(label, value):
    print(f"\n{label}")
    if isinstance(value, list):
        for row in value:
            print(f"  {dict(row)}")
    else:
        print(f"  {dict(value) if value else value}")


def main():
    conn = get_connection()
    initialize_db(conn)
    create_views(conn)

    genres = GenreDAO(conn)
    books = BookDAO(conn)
    members = MemberDAO(conn)
    loans = LoanDAO(conn)
    stats = StatsDAO(conn)

    print("=" * 60)
    print("INSERTS")
    print("=" * 60)

    fiction = genres.create("Fiction")
    mystery = genres.create("Mystery")
    show("Created genres:", [fiction, mystery])

    book1 = books.create("The Hobbit", "J.R.R. Tolkien", 1937, fiction["genre_id"], 3)
    book2 = books.create("Gone Girl", "Gillian Flynn", 2012, mystery["genre_id"], 2)
    show("Created books:", [book1, book2])

    today = datetime.date.today()
    alice = members.create("Alice Kapoor", "alice@example.com", today)
    ben = members.create("Ben Ortiz", "ben@example.com", today)
    show("Created members:", [alice, ben])

    # one current loan, one already overdue so the overdue view has data
    loan1 = loans.create(
        book1["book_id"], alice["member_id"], today, today + datetime.timedelta(days=14)
    )
    loan2 = loans.create(
        book2["book_id"], ben["member_id"],
        today - datetime.timedelta(days=30),
        today - datetime.timedelta(days=16),
    )
    show("Created loans:", [loan1, loan2])

    print("\n" + "=" * 60)
    print("READ / UPDATE / DELETE  (on genre)")
    print("=" * 60)

    show("Read genre by id:", genres.get_by_id(fiction["genre_id"]))

    updated = genres.update(fiction["genre_id"], "Literary Fiction")
    show("Updated genre:", updated)

    scratch = genres.create("Temporary")
    show("Genre before delete:", scratch)
    deleted = genres.delete(scratch["genre_id"])
    show("Deleted genre (returned row):", deleted)
    show("All genres now:", genres.get_all())

    print("\n" + "=" * 60)
    print("LOANS")
    print("=" * 60)

    show("Active loans (not yet returned):", loans.get_active_loans())

    returned = loans.return_book(loan1["loan_id"], today)
    show("Returned loan1:", returned)
    show("Active loans after return:", loans.get_active_loans())

    print("\n" + "=" * 60)
    print("STATISTICS VIEWS")
    print("=" * 60)

    show("Most loaned genres:", stats.most_loaned_genres())
    show("Most active members:", stats.most_active_members())
    show("Overdue loans:", stats.overdue_loans())

    conn.close()


if __name__ == "__main__":
    main()
