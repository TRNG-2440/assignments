--clean up
DROP SCHEMA book CASCADE
--setup
CREATE SCHEMA book;

--create tables
CREATE TABLE book.genres (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(50) NOT NULL

);

CREATE TABLE book.books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    pub_year INT NOT NULL,
    genre_id INT NOT NULL REFERENCES book.genres (genre_id),
    copies INT DEFAULT 1
);

CREATE TABLE book.members (
    member_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    date_joined DATE NOT NULL
);

CREATE TABLE book.loan (
    loan_id SERIAL PRIMARY KEY,
    book_id INT NOT NULL REFERENCES book.books (book_id),
    member_id INT NOT NULL REFERENCES book.members (member_id),
    loan_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE NULL
);
