CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_name VARCHAR(255) NOT NULL,
    publication_year INTEGER CHECK (publication_year > 0),
    genre_id INTEGER NOT NULL,
    total_copies INTEGER NOT NULL CHECK (total_copies >= 0),
    FOREIGN KEY (genre_id) REFERENCES genres (genre_id)
);

CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    join_date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE loans (
    loan_id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    loan_date DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books (book_id) ,
    FOREIGN KEY (member_id) REFERENCES members (member_id),
    CHECK (return_date IS NULL OR return_date >= loan_date),
    CHECK (due_date >= loan_date)
);