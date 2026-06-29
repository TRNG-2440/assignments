# Exercise — Library DAO

## Overview

In this exercise you will build a **Data Access Object (DAO)** layer for a library management system. You will design and create the database schema, implement standard CRUD operations in Python, and connect those operations to a live SQL database of your choice.

You may use **SQLite, PostgreSQL, or another SQL RDBMS** of your choice. Do not spend time on database setup — use whatever you are most comfortable connecting to from Python.

---

## Schema

Your database must implement the following four tables. Column names, types, and constraints are yours to decide, but the tables must capture at minimum the fields described below.

**Genre**
- A unique identifier
- A genre name (e.g. Fiction, Non-Fiction, Mystery)

**Book**
- A unique identifier
- A title
- An author name
- A publication year
- A reference to a Genre
- A total copy count (how many physical copies the library owns)

**Member**
- A unique identifier
- A full name
- An email address
- A join date

**Loan**
- A unique identifier
- A reference to a Book
- A reference to a Member
- A loan date
- A due date
- A return date (nullable — null indicates the book has not yet been returned)

*Your submission must include the DDL statements that create these tables. These may be provided as a standalone `.sql` file, or as an `initialize_db()` function called from your Python code.*

---

## Requirements

### 1. Database Connection

Create a module or class responsible for managing the database connection. It should expose a way to get a connection or cursor that can be used by your DAO classes.

### 2. DAO Classes

Implement a separate DAO class for each of the four tables: `GenreDAO`, `BookDAO`, `MemberDAO`, and `LoanDAO`. Each DAO must implement the following CRUD operations:

**GenreDAO**
- `create(name)` — insert a new genre, return the created record
- `get_by_id(genre_id)` — return a single genre by its ID
- `get_all()` — return all genres
- `update(genre_id, name)` — update the genre name, return the updated record
- `delete(genre_id)` — delete a genre by its ID

**BookDAO**
- `create(title, author, publication_year, genre_id, copy_count)` — insert a new book, return the created record
- `get_by_id(book_id)` — return a single book by its ID
- `get_all()` — return all books
- `update(book_id, title, author, publication_year, genre_id, copy_count)` — update all fields on a book, return the updated record
- `delete(book_id)` — delete a book by its ID

**MemberDAO**
- `create(full_name, email, join_date)` — insert a new member, return the created record
- `get_by_id(member_id)` — return a single member by their ID
- `get_all()` — return all members
- `update(member_id, full_name, email, join_date)` — update all fields on a member, return the updated record
- `delete(member_id)` — delete a member by their ID

**LoanDAO**
- `create(book_id, member_id, loan_date, due_date)` — insert a new loan record, return the created record
- `get_by_id(loan_id)` — return a single loan by its ID
- `get_all()` — return all loans
- `get_active_loans()` — return all loans where the return date is null
- `return_book(loan_id, return_date)` — update the return date on a loan record, return the updated record
- `delete(loan_id)` — delete a loan by its ID

### 3. Parameterized Queries

All SQL statements must use **parameterized queries** for values — do not use string formatting or string concatenation to inject values into SQL statements. Column names and table names may appear as literals in your SQL strings, but user-supplied or variable data must always be passed as parameters.

### 4. Main Script

Provide a `main.py` (or equivalent entry point) that demonstrates each DAO in action. It should:

- Initialize the database
- Insert at least two records into each table
- Demonstrate a read, update, and delete operation on at least one table

---

## Submission

Your submission should include at minimum:

- DDL statements (`.sql` file or `initialize_db()` function)
- One module per DAO class, or a single module containing all four
- A `main.py` entry point demonstrating the DAO layer
- A `requirements.txt` if any third-party packages are used

---

## Stretch Goal 1 — FastAPI REST Endpoints

Wire your DAO layer to a REST API using **FastAPI**. For each DAO, implement HTTP endpoints that correspond to its CRUD operations, with appropriate request and response models defined using **Pydantic**.

Your API must include at minimum:

**Genre**
- `GET /genres` — return all genres
- `GET /genres/{genre_id}` — return a single genre
- `POST /genres` — create a new genre
- `PUT /genres/{genre_id}` — update a genre
- `DELETE /genres/{genre_id}` — delete a genre

**Book**
- `GET /books` — return all books
- `GET /books/{book_id}` — return a single book
- `POST /books` — create a new book
- `PUT /books/{book_id}` — update a book
- `DELETE /books/{book_id}` — delete a book

**Member**
- `GET /members` — return all members
- `GET /members/{member_id}` — return a single member
- `POST /members` — create a new member
- `PUT /members/{member_id}` — update a member
- `DELETE /members/{member_id}` — delete a member

**Loan**
- `GET /loans` — return all loans
- `GET /loans/active` — return all active loans
- `GET /loans/{loan_id}` — return a single loan
- `POST /loans` — create a new loan
- `PATCH /loans/{loan_id}/return` — mark a loan as returned
- `DELETE /loans/{loan_id}` — delete a loan

Each endpoint should return an appropriate HTTP status code. Request and response bodies should be defined as Pydantic models — do not return raw dictionaries or untyped responses.

---

## Stretch Goal 2 — Library Statistics Views

Create SQL views for each of the following statistics. The SQL statements to create these views should be provided either as a standalone `.sql` file or as a `create_views()` utility function called from your Python code.

For each view, also implement a corresponding Python method that queries it and returns the result.

**1. Most Frequently Loaned Genre**

Create a view that returns each genre alongside the total number of times a book of that genre has been loaned, ordered from most to least loaned. *Note: this will require joining across Loan, Book, and Genre.*

**2. Most Active Members**

Create a view that returns each member alongside their total loan count, ordered from most to least active. Members with no loans should still appear in the result with a count of zero.

**3. Overdue Loans**

Create a view that returns all loans which are currently overdue — that is, loans where the return date is null and the due date has passed. The result should include the member's name, the book title, the due date, and the number of days the loan is overdue. *Note: date arithmetic syntax varies between databases — for example, PostgreSQL uses `CURRENT_DATE - due_date`, SQLite uses `julianday('now') - julianday(due_date)`, and MySQL uses `DATEDIFF(CURDATE(), due_date)`. Refer to the documentation for your chosen database.*
