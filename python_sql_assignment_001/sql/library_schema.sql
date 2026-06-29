



CREATE TABLE genre (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE book (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_name VARCHAR(255) NOT NULL,
    publication_year INTEGER,
    genre_id INTEGER NOT NULL,
    copies_count INTEGER NOT NULL CHECK (copies_count >= 0),
    
    CONSTRAINT fk_genre_id FOREIGN KEY (genre_id) REFERENCES genre(genre_id) ON DELETE RESTRICT

);

CREATE TABLE member (
    member_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email_address VARCHAR(255) UNIQUE NOT NULL,
    join_date DATE NOT NULL
);

CREATE TABLE loan (
    loan_id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    loan_date DATE NOT NULL,
    due_date DATE NOT NULL,
    returned_date DATE DEFAULT NULL,

    CONSTRAINT fk_book_id FOREIGN KEY (book_id) REFERENCES book(book_id) ON DELETE CASCADE,
    CONSTRAINT fk_member_id FOREIGN KEY (member_id) REFERENCES member(member_id) ON DELETE CASCADE
);