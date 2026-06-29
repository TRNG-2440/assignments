CREATE TABLE IF NOT EXISTS genre(
    genre_id INTEGER PRIMARY KEY,
    genre_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS book(
    book_id INTEGER PRIMARY KEY,
    book_title TEXT NOT NULL,
    book_author TEXT NOT NULL,
    book_year INT NOT NULL,
    book_genre INT NOT NULL,
    book_copies INT NOT NULL,
    FOREIGN KEY (book_genre) REFERENCES genre(genre_id)
);

CREATE TABLE IF NOT EXISTS member(
    member_id INTEGER PRIMARY KEY,
    member_name TEXT NOT NULL,
    member_email TEXT NOT NULL UNIQUE,
    join_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS loan(
    loan_id INTEGER PRIMARY KEY,
    loan_book INTEGER NOT NULL,
    loan_member INTEGER NOT NULL,
    loan_date DATE NOT NULL,
    loan_due DATE NOT NULL,
    loan_return_date DATE,
    FOREIGN KEY (loan_book) REFERENCES book(book_id),
    FOREIGN KEY (loan_member) REFERENCES member(member_id)
);

DELETE FROM loan;
DELETE FROM book;
DELETE FROM member;
DELETE FROM genre;