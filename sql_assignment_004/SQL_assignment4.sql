CREATE TABLE IF NOT EXISTS books(
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title STRING,
    author INTEGER,
    publication INTEGER,
    page_count INTEGER
);

INSERT INTO books (title, author, publication, page_count)
VALUES ('The Adventures of Tom Sawyer', 1004, 1876, 275);



DELETE FROM books
WHERE author = 1004;