DROP SCHEMA IF EXISTS lfields001 CASCADE;

CREATE SCHEMA IF NOT EXISTS lfields001;

CREATE TABLE IF NOT EXISTS lfields001.Genre (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS lfields001.Book (
    book_id SERIAL PRIMARY KEY,
    genre_id INT NOT NULL,
    title VARCHAR(64),
    author VARCHAR(64),
    publication_year SMALLINT,
    inventory SMALLINT,
    CONSTRAINT genre_id_fk FOREIGN KEY (genre_id) REFERENCES lfields001.Genre(genre_id)
);

CREATE TABLE IF NOT EXISTS lfields001.Member (
    member_id SERIAL PRIMARY KEY,
    member_name VARCHAR(64),
    email VARCHAR(64),
    date_joined DATE
);

CREATE TABLE IF NOT EXISTS lfields001.Loan (
    loan_id SERIAL PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    date_loaned DATE,
    date_due DATE NOT NULL,
    date_returned DATE DEFAULT NULL,
    CONSTRAINT book_id_fk FOREIGN KEY (book_id) REFERENCES lfields001.Book(book_id),
    CONSTRAINT member_id_fk FOREIGN KEY (member_id) REFERENCES lfields001.Member(member_id)
);