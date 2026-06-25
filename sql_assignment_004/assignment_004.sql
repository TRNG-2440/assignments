-- the fastest, most resource efficient way to do this:
-- TRUNCATE TABLE books;

-- a more precise method
DELETE FROM books
WHERE books.author = (
    SELECT author_id FROM author WHERE author_name = 'Mark Twain'
);