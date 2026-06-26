CREATE TABLE IF NOT EXISTS author(
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT
);

CREATE TABLE IF NOT EXISTS books(
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title STRING,
    author INTEGER,
    publication INTEGER,
    page_count INTEGER,
    FOREIGN KEY (author) REFERENCES author(author_id)
);

SELECT SUM(page_count) AS stephen_pages
FROM books
WHERE author = 1005;