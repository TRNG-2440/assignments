DROP TABLE IF EXISTS genre CASCADE;
CREATE TABLE genre (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(255) NOT NULL,
    CONSTRAINT genre_name_uniq UNIQUE(genre_name)
);

DROP TABLE IF EXISTS member CASCADE;
CREATE TABLE member (
    member_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    join_date DATE NOT NULL,
    CONSTRAINT email_uniq UNIQUE(email)
);

DROP TABLE IF EXISTS book CASCADE;
CREATE TABLE book (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_name VARCHAR(255) NOT NULL,
    publication_year CHAR(4) NOT NULL,
    genre_id INTEGER NOT NULL,
    total_copies INTEGER NOT NULL,
    FOREIGN KEY(genre_id) REFERENCES genre(genre_id)
);

DROP TABLE IF EXISTS loan CASCADE;
CREATE TABLE loan (
    loan_id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    loan_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY(book_id) REFERENCES book(book_id),
    FOREIGN KEY(member_id) REFERENCES member(member_id)
);