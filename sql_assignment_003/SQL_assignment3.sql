CREATE TABLE IF NOT EXISTS books(
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title STRING,
    author INTEGER,
    publication INTEGER,
    page_count INTEGER
);


INSERT INTO books (title, author, publication, page_count)
VALUES ('Homage to Catalonia', 1002, 1938, 368);

