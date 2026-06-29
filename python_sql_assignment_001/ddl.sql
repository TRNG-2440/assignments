--clean up
DROP SCHEMA IF EXISTS books CASCADE;
--setup
CREATE SCHEMA books;

--create tables
CREATE TABLE books.genre (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(50) NOT NULL

);

CREATE TABLE books.book (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    pub_year INT NOT NULL,
    genre_id INT NOT NULL REFERENCES books.genre (genre_id),
    copies INT DEFAULT 1
);

CREATE TABLE books.member (
    member_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    date_joined DATE NOT NULL
);

CREATE TABLE books.loan (
    loan_id SERIAL PRIMARY KEY,
    book_id INT NOT NULL REFERENCES books.book (book_id),
    member_id INT NOT NULL REFERENCES books.member (member_id),
    loan_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE NULL
);
