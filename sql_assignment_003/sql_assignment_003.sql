-- Create Tables
CREATE TABLE Author (
    author_id INT PRIMARY KEY,
    author_name VARCHAR(100) NOT NULL
);

CREATE TABLE Books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    author INT,
    publication INT,
    page_count INT,
    FOREIGN KEY (author) REFERENCES Author(author_id)
);

-- Add book created by George Orwell
INSERT INTO Books (title, author, publication, page_count)
VALUES ('Very good book!', 1002, 2072, 10000);