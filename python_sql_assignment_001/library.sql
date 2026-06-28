-- schema
DROP SCHEMA IF EXISTS library CASCADE;

CREATE SCHEMA library;

-- genre
CREATE TABLE library.genre (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(30) UNIQUE NOT NULL
);

-- book
CREATE TABLE library.book (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(80),
    author VARCHAR(50),
    publication_year INTEGER,
    genre_id INTEGER REFERENCES library.genre,
    copy_count INTEGER CHECK (copy_count >= 0)
);

-- member
CREATE TABLE library.member (
    member_id SERIAL PRIMARY KEY,
    member_name VARCHAR(50),
    email VARCHAR(50),
    join_date DATE
);

-- loan
CREATE TABLE library.loan (
    loan_id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES library.book,
    member_id INTEGER REFERENCES library.member,
    loan_date DATE,
    due_date DATE,
    return_date DATE
);