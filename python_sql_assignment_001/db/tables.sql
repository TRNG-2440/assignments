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
    available_copies INTEGER NOT NULL,
    FOREIGN KEY(genre_id) REFERENCES genre(genre_id),
    CONSTRAINT valid_available_copies_check CHECK (available_copies >= 0 AND available_copies <= total_copies)
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

-- Sample data
INSERT INTO genre (genre_name) VALUES
    ('Mystery'),
    ('Romance');

INSERT INTO member (name, email, join_date) VALUES
    ('Tom Cruise', 'tomcruz@email.com', '2010-09-22'),
    ('Elizabeth Benett', 'lizbenett@email.com', '1945-03-12');

INSERT INTO book (title, author_name, publication_year, genre_id, total_copies, available_copies) VALUES
    ('The Rosie Project', 'Graeme Simsion', 2013, 2, 1, 0),
    ('The Devotion of Suspect X', 'Higashino Keigo', 2005, 1, 3, 2);

INSERT INTO loan (book_id, member_id, loan_date, due_date, return_date) VALUES
    (1, 1, '2026-06-15', '2026-06-22', '2026-06-20'),
    (2, 1, '2026-06-24', '2026-07-01', NULL);